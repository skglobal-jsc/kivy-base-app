from threading import Thread

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty, StringProperty

from kivymd.button import MDRaisedButton
from kivymd.label import MDLabel

Builder.load_string('''
#:import MDSpinner kivymd.spinner.MDSpinner

<ProcessWidget>:
    canvas:
        Color:
            rgba: app.theme_cls.bg_darkest
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: 10,10,10,10
    size_hint: (None, None)
    size: dp(220), dp(220)
    auto_dismiss: False
    FloatLayout:
        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(50), dp(50)
            active: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        MDLabel:
            text: "Please wait a moment"
            font_style: 'Subhead'
            pos_hint: {'center_x': 0.65, 'center_y': 0.25}
        MDFlatButton:
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            text: "Cancel"
            on_release: root.stop_target()
''')

class ProcessWidget(ModalView):

    def __init__(self, target=None, name=None, targs=(), tkwargs={}, **kwargs):
        super(ProcessWidget, self).__init__(**kwargs)
        self.target = target
        self.threading_image = Thread(target=self.run_target,
                                        name=name, args=targs, kwargs=tkwargs)

    def run_target(self, *args, **kwargs):
        self.target(*args, **kwargs)
        self.dismiss()

    def stop_target(self):
        self.threading_image.join(timeout=0.5)
        self.dismiss()

    def on_open(self):
        self.threading_image.start()


if __name__ == '__main__':
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.popup import Popup
    from time import sleep

    from kivy.app import App
    from kivymd.theming import ThemeManager

    class MainApp(App):
        theme_cls = ThemeManager()

        def build(self):
            layout = BoxLayout()
            btn = MDRaisedButton(text='Click me',
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            btn.bind(on_release=lambda x:
                        ProcessWidget(target=lambda : sleep(10)).open())
            layout.add_widget(btn)

            return layout
    MainApp().run()
