import socket
import base64
import ssl
import re
from SMTPException import *
from Constants import *


class SMTP:
    def __init__(self, smtp_server, encoding="utf-8", encrypt=False):
        self.smtp_server = smtp_server
        self.encoding = encoding
        self.auth_protocols = []
        self.encrypt = encrypt
        self.connect()
        LOGGER.register(log_level.INFO, "Connected to the server")

    def connect(self):
        def connect_and_recv(sock):
            try:
                sock.connect(self.smtp_server)
                sock.recv(BUFFER_SIZE)
            except Exception as e:
                raise SMTPConnectionError()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (not self.encrypt):
            LOGGER.register(log_level.INFO, "Connect to server ({0}, {1}) without encryption".format(*self.smtp_server))
            self.socket.settimeout(3)
            try:
                connect_and_recv(self.socket)
            except socket.timeout:
                self.encrypt = True
                self.connect()
        else:
            LOGGER.register(log_level.INFO, "Connect to server ({0}, {1}) with encryption ssl.PROTOCOL_SSLv23".format(*self.smtp_server))
            self.socket = ssl.wrap_socket(
                self.socket, ssl_version=ssl.PROTOCOL_SSLv23)
            connect_and_recv(self.socket)

    def send(self, data):
        self.socket.sendall(data + b"\r\n")

    def recv(self):
        def recv_code():
            data = self.socket.recv(BUFFER_SIZE)
            while (len(data) < 4):
                data += self.socket.recv(BUFFER_SIZE)
            return data

        def recvall():
            data = recv_code()
            while (data[3] == b'-'):
                data += recv_code()
            return data

        data = recvall().decode(self.encoding)
        code, response = data[:3], re.sub(r'^-', '', data[3:])
        return int(code), response

    def ehlo(self):
        code, response = self.execute("EHLO Daniel")
        if code != CODE_ACCEPTED:
            raise SMTPInitSessionError(self.smtp_server)
        for line in response.split('\r\n'):
            if "AUTH" in line:
                self.auth_protocols = list(
                    filter(
                        lambda x: x == "LOGIN" or x == "PLAIN",
                        line.split()[
                            1:]))

    def execute(self, command, is_message=False, auth=False):
        if not isinstance(command, bytes):
            command = command.encode(self.encoding)

        self.send(command)
        if not is_message:
            code, response = self.recv()
            if not auth:
                LOGGER.register(log_level.INFO, "exectuing command {0}".format(command))
            LOGGER.register(log_level.INFO, "{code} {message}".format(code=code, message=response))
            return code, response

    def auth_plain(self, login, password):
        code, response = self.execute("AUTH PLAIN")
        if code != CODE_OK_CAN_CONTINUE:
            return code, response
        return self.execute(base64.b64encode(
            ("\0%s\0%s" % (login, password)).encode(self.encoding)), auth=True)

    def auth_login(self, login, password):
        code, response = self.execute("AUTH LOGIN")
        if code != CODE_OK_CAN_CONTINUE:
            return code, response
        code, response = self.execute(
            base64.b64encode(
                login.encode(
                    self.encoding)))
        if code != CODE_OK_CAN_CONTINUE:
            return code, response
        return self.execute(base64.b64encode(password.encode(self.encoding)), auth=True)

    def auth(self, login, password):
        if self.auth_protocols is None or len(self.auth_protocols) == 0:
            raise SMTPAuthProtocolError()

        if self.auth_protocols[0] == "PLAIN":
            code, response = self.auth_plain(login, password)
        else:
            code, response = self.auth_login(login, password)
        if code != CODE_AUTH_SUCCEEDED:
            raise SMTPAuthError()
        return code, response

    def mail(self, sender):
        code, response = self.execute("MAIL FROM:<%s>" % (sender))
        if code != CODE_ACCEPTED:
            raise SMTPMailSenderError()
        return code, response

    def rcpt(self, recipient):
        code, response = self.execute("RCPT TO:<%s>" % (recipient))
        return code, response

    def send_mesg(self, sender, recipients, mesg):
        self.mail(sender)
        errors = {}
        for recipient in recipients:
            code, response = self.rcpt(recipient)
            if code not in [CODE_ACCEPTED, CODE_USER_NOT_LOCAL_FORWARDING]:
                errors[recipient] = code, response

        code, response = self.execute("DATA")
        if code != CODE_DATA:
            raise SMTPDataError()
        self.execute(mesg, is_message=True)
        code, response = self.execute(".")
        if code != CODE_ACCEPTED:
            raise SMTPEndData()


        return errors

    def close(self):
        self.execute("QUIT")
        self.socket.close()
