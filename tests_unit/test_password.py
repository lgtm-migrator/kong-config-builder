from unittest import TestCase
from kong_config_builder.password import PasswordManager


class TestPassword(TestCase):
    def test_should_generate_password(self):
        password = PasswordManager.generate(10)
        self.assertEqual(len(password), 10)
