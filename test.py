import os
from os.path import dirname, join
import shutil
import unittest

from get_secret import CastException, CleanException, get


class GetSecretTestCase(unittest.TestCase):
    secret_dir = join(dirname(__file__), 'test_secrets')

    def make_secret(self, key, value):
        os.makedirs(self.secret_dir, exist_ok=True)
        with open(join(self.secret_dir, key), 'w') as _file:
            _file.write(value)

    def remove_secrets(self):
        shutil.rmtree(self.secret_dir)

    def setUp(self):
        self.make_secret('DB_HOST', 'db')
        self.make_secret('DB_PORT', '5432')
        self.make_secret('BALANCE', '52.61')
        self.make_secret('SEND_EMAILS', 'True')
        self.make_secret('TITLE', 'some title here ')
        self.make_secret('DESCRIPTION', 'some \ndescription here \r\n')
        os.environ['HOSTNAME'] = 'localhost'
        os.environ['MAX_WORKERS'] = '4'
        os.environ['PERCENT_CHANGE'] = '15.3'
        os.environ['DISABLE_CACHE'] = 'false'

    def tearDown(self):
        self.remove_secrets()
        os.environ.pop('HOSTNAME')
        os.environ.pop('MAX_WORKERS')
        os.environ.pop('PERCENT_CHANGE')
        os.environ.pop('DISABLE_CACHE')

    def test_string_secret_1(self):
        value = get('DB_HOST',
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 'db')
        self.assertIsInstance(value, str)

    def test_string_secret_2(self):
        value = get('HOSTNAME',
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 'localhost')
        self.assertIsInstance(value, str)

    def test_int_secret_1(self):
        value = get('DB_PORT',
                    to_type=int,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 5432)
        self.assertIsInstance(value, int)

    def test_int_secret_2(self):
        value = get('MAX_WORKERS',
                    to_type=int,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 4)
        self.assertIsInstance(value, int)

    def test_float_secret_1(self):
        value = get('BALANCE',
                    to_type=float,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 52.61)
        self.assertIsInstance(value, float)

    def test_float_secret_2(self):
        value = get('PERCENT_CHANGE',
                    to_type=float,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 15.3)
        self.assertIsInstance(value, float)

    def test_bool_secret_1(self):
        value = get('SEND_EMAILS',
                    to_type=bool,
                    secret_dir=self.secret_dir)

        self.assertTrue(value)
        self.assertIsInstance(value, bool)

    def test_bool_secret_2(self):
        value = get('DISABLE_CACHE',
                    to_type=bool,
                    secret_dir=self.secret_dir)

        self.assertFalse(value)
        self.assertIsInstance(value, bool)

    def test_cleaned_value_1(self):
        value = get('TITLE',
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 'some title here')
        self.assertIsInstance(value, str)

    def test_cleaned_value_2(self):
        value = get('DESCRIPTION',
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 'some description here')
        self.assertIsInstance(value, str)

    def test_cast_exception(self):
        with self.assertRaises(CastException):
            get('DB_HOST',
                to_type=int,
                exception=True,
                secret_dir=self.secret_dir)

    def test_cast_exception_supressed(self):
        value = get('DB_HOST',
                    to_type=int,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, None)

    def test_clean_exception(self):
        with self.assertRaises(CleanException):
            get('DB_HOST',
                clean_fn=lambda x: int(x),
                exception=True,
                secret_dir=self.secret_dir)

    def test_clean_exception_supressed(self):
        value = get('DB_HOST',
                    clean_fn=lambda x: int(x),
                    secret_dir=self.secret_dir)

        self.assertEqual(value, None)

    def test_default_not_found(self):
        value = get('DB_USER',
                    default='root',
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 'root')

    def test_default_on_cast_exception(self):
        value = get('API_KEY',
                    default=3342,
                    to_type=int,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 3342)
        self.assertIsInstance(value, int)

    def test_default_on_clean_exception(self):
        value = get('SEND_EMAILS',
                    default=False,
                    clean_fn=lambda x: int(x),
                    secret_dir=self.secret_dir)

        self.assertFalse(value)

    def test_no_env(self):
        value = get('HOSTNAME',
                    env=False,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, None)

    def test_no_env_with_default(self):
        value = get('HOSTNAME',
                    default='server',
                    env=False,
                    secret_dir=self.secret_dir)

        self.assertEqual(value, 'server')
        self.assertIsInstance(value, str)


if __name__ == '__main__':
    unittest.main()
