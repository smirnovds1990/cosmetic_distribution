import unittest
from werkzeug.exceptions import NotFound, InternalServerError

from cosmetic_distribution import app


class TestCustomErrorPages(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = app.test_client()

    def test_page_not_found(self):
        response = self.client.get('/test_nonexisted_url')
        self.assertEqual(response.status_code, NotFound.code)

    def test_internal_error(self):
        response = self.client.get('/cause_internal_error')
        self.assertEqual(response.status_code, InternalServerError.code)
