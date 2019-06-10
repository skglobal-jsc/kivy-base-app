
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
import inspect
from functools import wraps
from datetime import datetime
import json
from time import sleep

from kivy.logger import Logger
from kivy.event import EventDispatcher
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

PORT = 8000
from utils.platform import IS_RELEASE

MY_IP = ''

if not IS_RELEASE:
    Log_P2P = Logger.info
else:
    Log_P2P = Logger.debug

def _catch_exception(func):
    @wraps(func)
    def f(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            Logger.exception('Catch Exception:')
    return f

class SocketP2P(object):
    '''
    A peer to peer socket server base on OSCPy
    '''
    server = None
    allow_finding = False
    is_host = False
    is_running = False

    config_data = ''

    _my_name = ''

    def get_my_name(self):
        return self._my_name

    def set_my_name(self, name):
        if name:
            self._my_name = name

    my_name = property(get_my_name, set_my_name)

    __events__ = (
        'on_create_server',
        'on_scan_device', 'on_found_device', 'on_device_hided',
        'on_connect_user', 'on_accepted_connection',
        'on_request_config', 'on_got_config',
        'on_new_device', 'on_delete_device'
    )
    _callback_collec = {}

    def __init__(self, port, bind_collection={}, **kwargs):
        # super(SocketP2P, self).__init__(**kwargs)

        self._port = port
        self._bind_collection = bind_collection
        self._bind_collection.update({
            '/probe': self._probe,
            '/found': self._found,
            '/hided': self._hided_host,
            '/get_conf': self._send_conf,
            '/conf': self._got_conf,
            '/new_device': self._new_device,
            '/delete_device': self._delete_device
        })
        for event in SocketP2P.__events__:
            self._callback_collec[event] = [getattr(self, event)]

        sock = socket.socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.settimeout(1)
        self._scan_client = OSCClient(
            address='255.255.255.255',
            port=self._port,
            sock=sock,
            encoding='utf8'
        )

        self.create_server()

    @_catch_exception
    def _identify_me(self, time):
        global MY_IP

        if time == self._time:
            self.server.unbind('/identify_me', self._identify_me)
            _, ip_address, _ = self.server.get_sender()
            MY_IP = ip_address
            Log_P2P(f'P2P: IP: {self.myip}')
            if self._my_name == '':
                self.my_name = ip_address

    def stop(self):
        if self.server:
            try:
                self.server.stop_all()
            except Exception as e:
                Logger.exception('P2P: On close')
        self.is_running = False

    def bind(self, **kwargs):
        for event, cb in kwargs.items():
            if event in SocketP2P.__events__:
                self._callback_collec[event].append(cb)

    def unbind(self, event, callback):
        if event in SocketP2P.__events__ and\
                callback in self._callback_collec[event]:
            self._callback_collec[event].remove(callback)

    def bind_address(self, address, callback):
        self.server.bind(address, callback)
        self._bind_collection[address] = callback

    def unbind_address(self, address):
        self.server.unbind(
            address,
            self._bind_collection.pop(address, None)
        )

    def dispatch(self, event, *args, **kwargs):
        if event in SocketP2P.__events__:
            args = [self]+list(args)
            for cb in self._callback_collec[event]:
                try:
                    cb(*args, **kwargs)
                except TypeError as tye:
                    Logger.exception(f'TypeError: {cb.__qualname__} with {args} {kwargs}')
                except Exception as e:
                    Logger.exception(f'P2P: Error in {cb.__qualname__}')

    @property
    def myip(self):
        return MY_IP

    @_catch_exception
    def create_server(self):
        self.stop()
        self.reset_data()

        # Fix [Errno 98] Address already in use
        sleep(0.01)

        self.server = OSCThreadServer(encoding='utf8')
        self.server.listen(address='0.0.0.0', port=self._port, default=True)

        for address, cb in self._bind_collection.items():
            self.server.bind(address, cb)

        self.server.bind('/identify_me', self._identify_me)
        self._time = str(datetime.now())
        try:
            self._scan_client.send_message('/identify_me', [self._time])
        except OSError:
            Logger.exception('P2P: No network')
            self.server.unbind('/identify_me', self._identify_me)
            return

        self.dispatch('on_create_server', self.server)
        self.is_running = True

    def reset_data(self):
        self.list_device = []
        self.list_name = {}
        self.waiting_list = []

    @_catch_exception
    def scan_device(self):
        self.dispatch('on_scan_device')
        self._scan_client.send_message(b'/probe', [])

    @_catch_exception
    def _probe(self):
        if self.allow_finding:
            Log_P2P('P2P: /probe')
            self.server.answer(b'/found', values=[MY_IP, self.my_name],
                                port=self._port)
        else:
            self.server.answer(b'/hided', values=[MY_IP],
                                port=self._port)

    @_catch_exception
    def _found(self, ip, ip_name):
        if ip != MY_IP and ip not in self.list_device\
                and ip not in self.waiting_list:
            Log_P2P(f'P2P: /found {ip}')
            self.waiting_list.append(ip)
            self.dispatch('on_found_device', ip, ip_name)

    @_catch_exception
    def _hided_host(self, ip):
        if ip in self.waiting_list:
            Log_P2P(f'P2P: /hided {ip}')
            self.waiting_list.remove(ip)
            self.dispatch('on_device_hided', ip)

    def connect_user(self, ip):
        if ip in self.waiting_list:
            self.dispatch('on_connect_user', ip)
            self.get_config(ip)

    @_catch_exception
    def send_to_all(self, address, data, list_ip=None, and_myip=False):
        if not isinstance(data, list):
            data - list(data)
        if not list_ip:
            list_ip = self.list_device.copy()
        if and_myip:
            list_ip += [self.myip]

        Log_P2P(f'P2P: send {address}\nData: {data}\nTo: {list_ip}')
        for other in list_ip:
            self.server.send_message(address, data,
                other, self._port)

    def generate_token(self, *args):
        return '1234'

    def handle_token(self, token):
        if token == '1234':
            return True
        else:
            return False

    def get_config(self, ip):
        self.server.send_message(
                    b'/get_conf', [MY_IP, self.generate_token(), self.my_name],
                    ip, self._port)

    @_catch_exception
    def _send_conf(self, ip, token, ip_name):
        if self.handle_token(token) and self.allow_finding:
            Log_P2P(f'P2P: /get_conf {ip}')

            if ip not in self.list_device:
                for other in self.list_device:
                    self.send_to_all('/new_device',
                        [MY_IP, self.generate_token(), ip, ip_name])
                self.list_device.append(ip)
                self.list_name[ip] = ip_name
                self.dispatch('on_accepted_connection', ip, ip_name)

            list_send = {MY_IP: self.my_name}
            list_send.update(self.list_name)
            self.server.answer(b'/conf',
                [MY_IP, self.generate_token(), self.config_data, json.dumps(list_send)],
                port=self._port)
            self.dispatch('on_request_config', ip)

    @_catch_exception
    def _got_conf(self, ip, token, config_data, list_device):
        if self.handle_token(token):
            Log_P2P(f'P2P: /conf {ip} with {list_device}')
            self.list_device = []
            for i, name in json.loads(list_device).items():
                if i != MY_IP:
                    self.list_device.append(i)
                    self.list_name[i] = name

            if ip in self.waiting_list:
                self.waiting_list.remove(ip)

            self.dispatch('on_got_config', ip, config_data)

    @_catch_exception
    def _new_device(self, ip, token, new_ip, ip_name):
        if self.handle_token(token) and new_ip not in self.list_device:
            Log_P2P(f'P2P: /new_device {new_ip} {ip_name}')
            if ip in self.waiting_list:
                self.waiting_list.remove(new_ip)
            self.list_device.append(new_ip)
            self.list_name[new_ip] = ip_name
            self.dispatch('on_new_device', new_ip, ip_name)

    def remove_device(self):
        self.send_to_all('/delete_device', [MY_IP, self.generate_token(), MY_IP],
                            and_myip=True)
        self.reset_data()

    @_catch_exception
    def _delete_device(self, ip, token, del_ip):
        if self.handle_token(token):
            Log_P2P(f'P2P: /delete_device {del_ip}')
            if del_ip in self.waiting_list:
                self.waiting_list.remove(del_ip)
            if del_ip in self.list_device:
                self.list_device.remove(del_ip)
            self.list_name.pop(del_ip, None)
            self.dispatch('on_delete_device', ip, del_ip)

    def on_create_server(self, ins, server): pass
    def on_scan_device(self, ins): pass
    def on_found_device(self, ins, ip, ip_name): pass
    def on_device_hided(self, ins, ip): pass
    def on_connect_user(self, ins, ip): pass
    def on_accepted_connection(self, ins, ip, ip_name): pass
    def on_request_config(self, ins, ip): pass
    def on_got_config(self, ins, ip, config_data): pass
    def on_new_device(self, ins, new_ip, ip_name): pass
    def on_delete_device(self, ins, ip, del_ip): pass

if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.button import Button
    from functools import partial
    from kivy.metrics import dp
    from kivy.clock import mainthread

    class P2PApp(App):
        connection = None

        def on_start(self):
            self.connection = SocketP2P(
                PORT,
                bind_address={
                    '/get_message': self._get_message,
                }
            )
            self.connection.bind(
                on_scan_device=lambda *args: self.root.ids.container.clear_widgets(),
                on_found_device=self.create_button,
                on_connect_user=self.on_connect_user,
                on_accepted_connection=self.on_accepted_connection
            )
            self.connection.allow_finding = True

        def on_stop(self):
            self.connection.stop()

        def send_message(self, text):
            if len(self.connection.list_device) == 0:
                return
            self.connection.send_to_all(
                b'/get_message', [self.connection.myip, text])
            self.root.ids.m_input.text += '\nYou send: ' + text
            self.root.ids.text_send.text = ''

        @_catch_exception
        def _get_message(self, ip, text):
            Log_P2P(f'P2P: /get_message {ip} send {text}')
            if ip != self.connection.myip and ip in self.connection.list_device:
                self.root.ids.m_input.text += '\n{}: {}'.format(ip, text)

        @mainthread
        def create_button(self, ins, ip, ip_name):
            bt = Button(text=ip, size_hint_y=None, height='60dp')
            bt.bind(on_release=lambda *x: self.connection.connect_user(bt.text))
            self.root.ids.container.add_widget(bt)

        def on_connect_user(self, ins, ip):
            self.root.ids.container.clear_widgets()
            self.root.ids.m_input.text += f'\n{ip} just joined the conversation'

        def on_accepted_connection(self, ins, ip, ip_name):
            self.root.ids.m_input.text += f'\nYou connect to {ip}'

        def build(self):
            return Builder.load_string('''
BoxLayout:
    orientation:'vertical'
    BoxLayout:
        orientation:'vertical'
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            Button:
                text: 'Restart '
                on_release:
                    app.connection.create_server()
            Button:
                text: 'Scan user'
                on_release: app.connection.scan_device()
        ScrollView:
            do_scroll_x: False
            StackLayout:
                id: container
                size_hint: 1, None
                height: self.minimum_height
                orientation:'lr-tb'
                padding: dp(20), dp(5), dp(20), dp(5)
                spacing: dp(8)
    BoxLayout:
        orientation:'vertical'
        ScrollView:
            canvas.before:
                Color:
                    rgba: .9,.9,.9,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            TextInput:
                id: m_input
                size_hint_y: None
                height: len(self._lines)*(self.line_height+dp(3))
                background_normal: ''
                background_active: ''
                background_color: 1, 1, 1, 0
                cursor_color: 0, 0, 0, 1
                text: ''
                foreground_color: 0, 0, 0, 0.7
                font_size: '18sp'
                readonly: True
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            TextInput:
                id: text_send
                oneline: True
            Button:
                size_hint_x: None
                width: dp(120)
                text: 'Send'
                on_release:
                    app.send_message(text_send.text)
''')

    P2PApp().run()
