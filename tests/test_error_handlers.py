import unittest
from werkzeug.exceptions import NotFound, InternalServerError

from cosmetic_distribution import create_app
from settings import TestConfig


class TestCustomErrorPages(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def test_page_not_found(self):
        response = self.client.get('/test_nonexisted_url')
        self.assertEqual(response.status_code, NotFound.code)
        html = response.get_data(as_text=True)
        self.assertIn('404', html)
        self.assertIn('Страница не найдена', html)

    def test_internal_error(self):
        response = self.client.get('/cause_internal_error')
        self.assertEqual(response.status_code, InternalServerError.code)
        html = response.get_data(as_text=True)
        self.assertIn('500', html)
        self.assertIn('Проблема на сервере', html)
