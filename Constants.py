import os
import json
from logger import *


LOGGER = Logger()

SMTP_SERVERS = {
    'google': ('smtp.gmail.com', 465),
    'yandex': ('smtp.yandex.ru', 465),
    'mail': ('smtp.mail.ru', 465)
}

BUFFER_SIZE = 1024

CODE_ACCEPTED = 250
CODE_DATA = 354
CODE_USER_NOT_LOCAL_FORWARDING = 251
CODE_OK_CAN_CONTINUE = 334
CODE_AUTH_SUCCEEDED = 235

COMMASPACE = ', '
PWD = os.path.abspath(os.curdir)

TYPES_MAP = json.loads(open("types_map.json", "r").read())
ENCODINGS_MAP = json.loads(open("encodings_map.json", "r").read())

LEN_LINE_MIME_CONTENT = 76


class MIME_constants:
    content_disposition = 'Content-Disposition'
    content_transfer_encoding = "Content-transfer-encoding"
    bit7 = '7bit'
    quoted_printable = 'quoted-printable'
    base64 = 'base64'
    bit8 = '8bit'
    binary = 'binary'
    mime_version = 'MIME-Version'

    content_type = 'Content-type'
    application = 'application'
    image = 'image'
    audio = 'audio'
    message = 'message'
    text = 'text'
    video = 'video'
    multipart = 'multipart'
