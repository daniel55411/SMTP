import SMTP
from Constants import *
from SMTPException import *
import unittest
from unittest.mock import patch


def start_smtp():
    return SMTP.SMTP(('smtp.gmail.com', 465), encrypt=True)


class SMTP_tests(unittest.TestCase):
    def test_connection(self):
        with self.assertRaises(SMTPConnectionError) as cm:
            SMTP.SMTP(('smtp.gml.com', 465))

    @patch.object(SMTP.SMTP, 'execute')
    def test_recv_ehlo_fail(self, execute):
        execute.return_value = (
            501, '5.5.4 Empty HELO/EHLO argument not allowed, closing connection.')
        smtp = start_smtp()
        with self.assertRaises(SMTPInitSessionError) as cm:
            smtp.ehlo()
        self.assertEqual(('smtp.gmail.com', 465), cm.exception.server)
        smtp.close()

    @patch.object(SMTP.SMTP, 'execute')
    def test_recv_ehlo_success(self, execute):
        execute.return_value = (250, (
            '250 smtp.gmail.com at your service, [128.75.98.44]\n'
            '250-SIZE 35882577\n'
            '250-8BITMIME\n'
            '250-AUTH LOGIN PLAIN XOAUTH2 PLAIN-CLIENTTOKEN OAUTHBEARER XOAUTH\n'
            '250-ENHANCEDSTATUSCODES\n'
            '250-PIPELINING\n'
            '250-CHUNKING\n'
            '250 SMTPUTF8\n'))
        smtp = start_smtp()
        smtp.ehlo()
        self.assertEqual(smtp.auth_protocols, ['LOGIN', 'PLAIN'])
        smtp.close()

    @patch.object(SMTP.SMTP, 'execute')
    def test_ehlo_without_auth(self, execute):
        execute.return_value = (250, (
            '250 smtp.gmail.com at your service, [128.75.98.44]\n'
            '250-SIZE 35882577\n'
            '250-8BITMIME\n'
            '250-ENHANCEDSTATUSCODES\n'
            '250-PIPELINING\n'
            '250-CHUNKING\n'
            '250 SMTPUTF8\n'))
        smtp = start_smtp()
        smtp.ehlo()
        with self.assertRaises(SMTPAuthProtocolError):
            smtp.auth('daniel', 'daniel')
        smtp.close()

    def auth(self, auth_func, auth_mode, response, auth_error):
        auth_func.return_value = response
        smtp = start_smtp()
        smtp.auth_protocols = [auth_mode]
        if auth_error:
            with self.assertRaises(SMTPAuthError):
                smtp.auth('test', 'test')
        else:
            self.assertEqual(smtp.auth('test', 'test'), response)
        smtp.close()

    @patch.object(SMTP.SMTP, 'auth_login')
    @patch.object(SMTP.SMTP, 'auth_plain')
    def test_auth_plain_and_login_error(self, auth_plain, auth_login):
        self.auth(
            auth_plain,
            'PLAIN',
            (535,
             '5.7.8 Username and Password not accepted. Learn more at'),
            True)
        self.auth(
            auth_login,
            'LOGIN',
            (535,
             '5.7.8 Username and Password not accepted. Learn more at'),
            True)

    @patch.object(SMTP.SMTP, 'auth_login')
    @patch.object(SMTP.SMTP, 'auth_plain')
    def test_auth_plain_and_login_accepted(self, auth_plain, auth_login):
        self.auth(auth_plain, 'PLAIN', (235, '5.7.8 Accepted'), False)
        self.auth(auth_login, 'LOGIN', (235, '5.7.8 Accepted'), False)

    @patch.object(SMTP.SMTP, 'execute')
    def test_sender_fail(self, execute):
        execute.return_value = (550, 'Mail Sender')
        smtp = start_smtp()
        with self.assertRaises(SMTPMailSenderError):
            smtp.mail('test')
        smtp.close()

    @patch.object(SMTP.SMTP, 'execute')
    def test_sender_accepted(self, execute):
        execute.return_value = response = (250, 'Accepted')
        smtp = start_smtp()
        self.assertEqual(smtp.mail('test'), response)
        smtp.close()

    @patch.object(SMTP.SMTP, 'execute')
    def _test_end_data(self, execute):
        execute.return_value = (550, 'SPAM')
        smtp = start_smtp()
        with self.assertRaises(SMTPEndData):
            smtp.execute('.')
        smtp.close()


if __name__ == '__main__':
    unittest.main()
