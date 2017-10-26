from MIME import *
from MIME import *


class Mail:
    def __init__(self, sender,
                 recipients,
                 subject,
                 message,
                 attachments=None,
                 text_encoding='utf-8',
                 text_subtype='plain'):
        self.mail = MIMEMultipart()
        self.mail['From'] = sender
        self.mail['Subject'] = subject
        self.mail['To'] = COMMASPACE.join(recipients)

        text = MIMEText(message, text_subtype, text_encoding)
        self.mail.attach(text)

        if attachments is not None:
            for attachment in attachments:
                filename = os.path.abspath(attachment).replace(PWD, '')
                path = os.path.abspath(attachment)
                if not os.path.isfile(path):
                    LOGGER.register(
                        log_level.WARNING,
                        "file '%s' don't exist" %
                        (filename))
                    print("file '%s' don't exist" %
                        (filename))
                    continue
                ctype, encoding = guess_type(path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                if maintype == 'text':
                    with open(path) as fp:
                        _attachment = MIMEText(fp.read(), subtype, 'utf-8')
                elif maintype == 'image':
                    with open(path, 'rb') as fp:
                        _attachment = MIMEImage(fp.read(), subtype)
                elif maintype == 'audio':
                    with open(path, 'rb') as fp:
                        _attachment = MIMEAudio(fp.read(), subtype)
                else:
                    with open(path, 'rb') as fp:
                        _attachment = MIMEBase(maintype, subtype)
                        _attachment.set_payload(fp.read())
                _attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(path))
                self.mail.attach(_attachment)

    def __str__(self):
        return self.mail.as_string()
