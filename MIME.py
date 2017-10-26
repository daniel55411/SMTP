import base64
import random

import re

from Constants import *
from MIMEException import *


class Content_Type:
    def __init__(self):
        self.headers = ''
        self.fields = {}
        self.kwargs = {}
        self.string = None

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __iter__(self):
        return iter(self.fields)

    def add_header(self, name_header, type, **kwargs):
        self.headers = '%s: %s; %s' % (name_header,
                                       type,
                                       COMMASPACE.join('%s="%s"' % (key, kwargs[key]) for key in kwargs)) + '\n' + self.headers

    def get_headers(self):
        return self.headers
    # evv0409@mail.ru
    def as_string(self):
        if self.string is None:
            result = ''
            self.add_header(
                MIME_constants.content_transfer_encoding,
                MIME_constants.bit8)
                # MIME_constants.base64)
            self.add_header(MIME_constants.mime_version, '1.0')
            self.add_header(
                MIME_constants.content_type,
                self.mime_type + '/' + self.subtype,
                **self.kwargs)
            if not isinstance(self.stream, bytes):
                raise MIMEWrongInstance(bytes)
            # self.stream = base64.b64encode(self.stream).decode()
            self.stream = re.sub(r'\.(?!\.)', '..', self.stream.decode())
            # self.stream = self.stream.decode().replace('.', '..')
            result += self.get_headers()
            result += '\n'.join("%s: %s" %
                                (key, self.fields[key]) for key in self.fields) + '\n'
            if (len(self.fields) != 0):
                result += '\n'
            result += '\n'.join(self.stream[offset: offset + LEN_LINE_MIME_CONTENT]
                                for offset in range(0, len(self.stream), LEN_LINE_MIME_CONTENT)) + '\n'
            self.string = result
            return result
        else:
            return self.string


class MIMEText(Content_Type):
    mime_type = 'text'

    def __init__(self, text, subtype='plain', charset='us-ascii'):
        super(MIMEText, self).__init__()
        if not isinstance(text, bytes):
            self.stream = text.encode(charset)
        else:
            self.stream = text
        self.subtype = subtype
        self.kwargs = {'charset': charset}


class MIMEAudio(Content_Type):
    mime_type = "audio"

    def __init__(self, stream, subtype='basic'):
        super(MIMEAudio, self).__init__()
        self.stream = stream
        self.subtype = subtype


class MIMEImage(Content_Type):
    mime_type = 'image'

    def __init__(self, stream, subtype='jpeg'):
        super(MIMEImage, self).__init__()
        self.stream = stream
        self.subtype = subtype


class MIMEVideo(Content_Type):
    mime_type = 'video'

    def __init__(self, stream, subtype='jpeg'):
        super(MIMEVideo, self).__init__()
        self.stream = stream
        self.subtype = subtype


class MIMEBase(Content_Type):
    def __init__(self, maintype, subtype):
        super(MIMEBase, self).__init__()
        self.maintype = maintype
        self.mime_type = maintype
        self.subtype = subtype
        self.stream = None

    def set_payload(self, data):
        if isinstance(data, bytes):
            self.stream = data
        else:
            raise MIMEWrongInstance(bytes)


class MIMEMultipart(Content_Type):
    mime_type = 'multipart'

    def __init__(self):
        super(MIMEMultipart, self).__init__()
        self.attachments = []
        self.subtype = "mixed"
        self.boundary = self.generate_boundary()
        self.kwargs = {"boundary": self.boundary}

    def generate_boundary(self):
        return '=' * 15 + ''.join([str(random.randint(1, 9))
                                   for i in range(19)]) + '=='

    def attach(self, MIMEObject):
        if not isinstance(MIMEObject, Content_Type):
            raise MIMEWrongInstance(Content_Type)
        self.attachments.append(MIMEObject)

    def as_string(self):
        if self.string is None:
            result = ''
            self.add_header(MIME_constants.mime_version, '1.0')
            self.add_header(
                MIME_constants.content_type,
                self.mime_type + '/' + self.subtype,
                **self.kwargs)
            result += self.get_headers()
            result += '\n'.join("%s: %s" %
                                (key, self.fields[key]) for key in self.fields) + '\n'
            if (len(self.fields) != 0):
                result += '\n'
            for attachment in self.attachments:
                result += '--' + self.boundary + '\n'
                result += attachment.as_string() + '\n'
            if len(self.attachments) != 0:
                result += '--' + self.boundary + '--'
            self.string = result
            return result
        else:
            return self.string


def guess_type(path):
    if not isinstance(path, str):
        raise MIMEWrongInstance(str)
    extension = os.path.splitext(path)[1]
    if extension in TYPES_MAP:
        return TYPES_MAP[extension], None
    elif extension in ENCODINGS_MAP:
        return None, ENCODINGS_MAP[extension]
    else:
        return 'application/octet-stream', None
