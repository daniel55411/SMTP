import unittest
from MIME import *
import base64
import re


class MIME_tests(unittest.TestCase):
    def test_guess_type_instance_fail(self):
        with self.assertRaises(MIMEWrongInstance):
            guess_type(1)

    def test_guess_type_py_file(self):
        self.assertEqual(guess_type('test.py'), ("text/x-python", None))

    def test_guess_type_arch_file(self):
        self.assertEqual(guess_type('test.tar.gz'), (None, "gzip"))

    def test_guess_type_unknown_file(self):
        self.assertEqual(guess_type('test.bin'),
                         ('application/octet-stream', None))

    def test_MIMEMultipart_attach_not_MIMEObject(self):
        with self.assertRaises(MIMEWrongInstance):
            mail = MIMEMultipart()
            mail.attach('123')

    def test_MIMEMultipart_attach_MIMEObject(self):
        mail = MIMEMultipart()
        result = []
        audio = MIMEAudio(b'')
        mail.attach(audio)
        result.append(audio)
        self.assertEqual(len(mail.attachments), 1)
        video = MIMEVideo(b'')
        mail.attach(video)
        result.append(video)
        self.assertEqual(len(mail.attachments), 2)
        self.assertEqual(mail.attachments, result)

    def test_MIMEObject_as_string_fail(self):
        audio = MIMEAudio('bad data')
        with self.assertRaises(MIMEWrongInstance):
            audio.as_string()

    def test_MIMEObject_as_string_success(self):
        audio = MIMEAudio(b'123')
        result = ('Content-type: audio/basic;\n'
                  'MIME-Version: 1.0;\n'
                  'Content-transfer-encoding: base64;\n\n' +
                  base64.b64encode(b'123').decode() + '\n')
        self.assertEqual(
            audio.as_string().replace(
                ' ', ''), result.replace(
                ' ', ''))

    def test_MIMEBase_set_payload_wrong_instance(self):
        with self.assertRaises(MIMEWrongInstance):
            base = MIMEBase('applacation', 'octet-stream')
            base.set_payload('bad_data')

    def test_MIMEBase_set_payload_success(self):
        base = MIMEBase('applacation', 'octet-stream')
        base.set_payload(b'bad_data')
        self.assertEqual(base.stream, b'bad_data')

    def test_genarate_boundary(self):
        mail = MIMEMultipart()
        boundary = mail.generate_boundary()
        self.assertIsInstance(boundary, str)
        self.assertIsNotNone(re.match(r'={15}\d{19}==', boundary))

    def test_get_and_add_header(self):
        mail = Content_Type()
        mail.add_header("test1_name", "test1_type", test1="test1")
        mail.add_header("test2_name", "test2_type")
        mail.add_header("test3_name", "test3_type", test1="test1")
        result = (
            'test3_name: test3_type; test1="test1"\n'
            'test2_name: test2_type;\n'
            'test1_name: test1_type; test1="test1"\n')
        self.assertEqual(
            mail.get_headers().replace(
                ' ', ''), result.replace(
                ' ', ''))

    def test_MIMEMultipart_as_string(self):
        mail = MIMEMultipart()
        mail.attach(MIMEAudio(b''))
        boundary_pattern = r'\={15}\d{19}=='
        pattern = (
            r'Content-type:\smultipart/mixed;\sboundary="' +
            boundary_pattern +
            '"')
        self.assertIsNotNone(re.match(pattern, mail.as_string()))


if __name__ == '__main__':
    unittest.main()
