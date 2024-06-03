import unittest

from .test_config import TestConfig
from cosmetic_distribution import app


class TestFormsCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()
