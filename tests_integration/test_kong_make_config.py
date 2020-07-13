import requests
from unittest import TestCase

HOST = "http://localhost:8080"

BASE_URL = HOST + "{}"


class TestIntegration(TestCase):

    def test_should_call_google_by_proxy(self):
        resource = "/"
        response = requests.get(BASE_URL.format(resource), timeout=1)
        self.assertEqual(200, response.status_code)

    def test_should_call_google_by_proxy_without_auth(self):
        resource = "/auth"
        response = requests.get(BASE_URL.format(resource), timeout=1)
        self.assertEqual(401, response.status_code)

    def test_should_call_google_by_proxy_with_auth(self):
        resource = "/auth?apikey=pass1234"
        response = requests.get(BASE_URL.format(resource), timeout=1)
        self.assertEqual(200, response.status_code)
