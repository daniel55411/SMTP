import os
import unittest
from main import save_msg, send_msg_with_options, print_options
from console import Options
import pickle


class main_test(unittest.TestCase):
    def test_print_options_args_instance(self):
        with self.assertRaises(AssertionError) as e:
            print_options('object')

    def test_save_msg_args_instance(self):
        with self.assertRaises(AssertionError) as e:
            save_msg('object')

    def test_send_msg_with_options_args_instance(self):
        with self.assertRaises(AssertionError) as e:
            send_msg_with_options('object')

    def test_save_msg(self):
        if os.path.exists('dump.pickle'):
            os.remove('dump.pickle')
        test = {'test': 'acc', 'asser': 1}
        options = Options(test)
        save_msg(options)
        self.assertTrue(os.path.exists('dump.pickle'))
        with open('dump.pickle', 'rb') as f:
            result = pickle.load(f)
            self.assertDictEqual(result, test)
        os.remove('dump.pickle')


if __name__ == '__main__':
    unittest.main()
