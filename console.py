from optparse import OptionParser
from Constants import *
import sys
import getpass


class Options(dict):
    __getattr__, __setattr__ = dict.get, dict.__setitem__


class Console:
    def __init__(self):
        self.parser = OptionParser("""\
SMTP client for sending message with attachments

\t%prog [options]

To enumerate, it is necessary for each object to specify the option
For example, -a fil1 -a file2
-r m@m.com -r a@a.com
			""")

        self.parser.add_option('--disable-logging',
                               action='store_true',
                               default=False,
                               help='Disable logging')

        self.parser.add_option('--subject',
                               type='string',
                               action='store',
                               default='',
                               help='Subject of mail')

        self.parser.add_option('-s', '--sender',
                               type='string',
                               action='store',
                               help='e-mail of Sender')

        self.parser.add_option('-r', '--recipients',
                               type='string',
                               action='append',
                               help='e-mails of recipients',
                               default=[],
                               dest='recipients')

        self.parser.add_option('-m', '--message',
                               type='string',
                               action='store',
                               help='Message')

        self.parser.add_option('-a', '--attachments',
                               type='string',
                               action='append',
                               default=[],
                               dest='attachments',
                               help='attachments')
        self.parser.add_option('--server',
                               type='string',
                               action='store',
                               help='Enter smtp server')

        self.parser.add_option('-p', '--port',
                               type='string',
                               action='store',
                               help='Enter port for smtp server')

        self.parser.add_option('--single',
                               action='store_true',
                               default=False,
                               help='Send to recipients separately')

        self.parser.add_option('--password',
                               action='store_true',
                               help='Password for sender')

        self.parser.add_option('--disable-encryption',
                               action='store_true',
                               default=False,
                               help='Disable encryption for connection SMTP-server')

    def parse_opt(self):
        options, args = self.parser.parse_args()
        sender = options.sender if options.sender is not None else input(
            "Sender: ")
        recipients = options.recipients if options.recipients != [
        ] else input("Recipients(separator is ' '): ").split()
        server = options.server if options.server is not None else input(
            "Server: ")
        port = int(
            options.port) if options.port is not None else int(
            input("Port: "))
        message = ''
        if options.message is not None:
            message = options.message
        else:
            print('Ctrl^D in Bash or Ctrl^Z in CMD to end write Message')
            for line in sys.stdin:
                message += line

        password = getpass.getpass("Password: ") if options.password else None
        subject = options.subject
        attachments = options.attachments
        single = options.single
        disable_logging = options.disable_logging
        disable_encryption = options.disable_encryption

        return Options({
            'disable_logging': disable_logging,
            'sender': sender,
            'password': password,
            'recipients': recipients,
            'attachments': attachments,
            'message': message,
            'single': single,
            'server': server,
            'subject': subject,
            'disable_encryption': disable_encryption,
            'port': port,
        })
