from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from http.client import HTTPMessage, LineTooLong, HTTPException
from http import HTTPStatus
from email.parser import Parser
_MAXLINE = 65536
_MAXHEADERS = 100
class myHandler(BaseHTTPRequestHandler):
    timeout = 200
    def do_GET(self):
        # print(self.headers._headers)
        # self.headers.get('Connection', "")
        print(self.headers)
        print(self.path)
        print('-'*10)
        print(self.rawdata)
        print('-'*10)
        self.send_response(200)
        self.send_header(b'Content-type',b'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"Hello World !")
        return
    def do_PUT(self):
        # print(self.headers._headers)
        # self.headers.get('Connection', "")
        print(self.headers)
        print(self.path)
        print('-'*10)
        print(self.rawdata)
        print('-'*10)
        self.send_response(200)
        self.send_header(b'Content-type',b'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"Hello World !")
        return
    def do_POST(self):
        # print(self.headers._headers)
        # self.headers.get('Connection', "")
        print(self.headers)
        print(self.path)
        print('-'*10)
        print(self.rawdata)
        print('-'*10)
        self.send_response(201)
        self.send_header(b'Content-type',b'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"Hello World !")
        return
    def parse_headers(self, fp, _class=HTTPMessage):
        headers = []
        while True:
            line = fp.readline(_MAXLINE + 1)
            if len(line) > _MAXLINE:
                raise LineTooLong("header line")
            headers.append(line)
            if len(headers) > _MAXHEADERS:
                raise HTTPException("got more than %d headers" % _MAXHEADERS)
            if line in (b'\r\n', b'\n', b''):
                break
        hstring = b''.join(headers).decode('iso-8859-1')
        self.rawdata = headers
        return Parser(_class=_class).parsestr(hstring)
    def parse_request(self):
        self.command = None  # set in case of error on the first line
        self.request_version = version = self.default_request_version
        self.close_connection = True
        requestline = str(self.raw_requestline, 'iso-8859-1')
        print(requestline)
        requestline = requestline.rstrip('\r\n')
        self.requestline = requestline
        words = requestline.split()
        if len(words) == 0:
            return False
        if len(words) >= 3:  # Enough to determine protocol version
            version = words[-1]
            try:
                if not version.startswith('HTTP/'):
                    raise ValueError
                base_version_number = version.split('/', 1)[1]
                version_number = base_version_number.split(".")
                # RFC 2145 section 3.1 says there can be only one "." and
                #   - major and minor numbers MUST be treated as
                #      separate integers;
                #   - HTTP/2.4 is a lower version than HTTP/2.13, which in
                #      turn is lower than HTTP/12.3;
                #   - Leading zeros MUST be ignored by recipients.
                if len(version_number) != 2:
                    raise ValueError
                version_number = int(version_number[0]), int(version_number[1])
            except (ValueError, IndexError):
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Bad request version (%r)" % version)
                return False
            if version_number >= (1, 1) and self.protocol_version >= "HTTP/1.1":
                self.close_connection = False
            if version_number >= (2, 0):
                self.send_error(
                    HTTPStatus.HTTP_VERSION_NOT_SUPPORTED,
                    "Invalid HTTP version (%s)" % base_version_number)
                return False
            self.request_version = version
        if not 2 <= len(words) <= 3:
            self.send_error(
                HTTPStatus.BAD_REQUEST,
                "Bad request syntax (%r)" % requestline)
            return False
        command, path = words[:2]
        if len(words) == 2:
            self.close_connection = True
            if command != 'GET':
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Bad HTTP/0.9 request type (%r)" % command)
                return False
        self.command, self.path = command, path
        # Examine the headers and look for a Connection directive.
        try:
            self.headers = self.parse_headers(self.rfile,
                                                     _class=self.MessageClass)
        except LineTooLong as err:
            self.send_error(
                HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
                "Line too long",
                str(err))
            return False
        except HTTPException as err:
            self.send_error(
                HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
                "Too many headers",
                str(err)
            )
            return False
        conntype = self.headers.get('Connection', "")
        if conntype.lower() == 'close':
            self.close_connection = True
        elif (conntype.lower() == 'keep-alive' and
              self.protocol_version >= "HTTP/1.1"):
            self.close_connection = False
        # Examine the headers and look for an Expect directive
        expect = self.headers.get('Expect', "")
        if (expect.lower() == "100-continue" and
                self.protocol_version >= "HTTP/1.1" and
                self.request_version >= "HTTP/1.1"):
            if not self.handle_expect_100():
                return False
        return True


myHandler.protocol_version = 'HTTP/1.0'
PORT_NUMBER = 8080
with ThreadingHTTPServer(('127.0.0.1', PORT_NUMBER), myHandler) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")

