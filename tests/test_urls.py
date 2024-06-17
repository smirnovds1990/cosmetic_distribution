import unittest
from werkzeug.security import generate_password_hash

from cosmetic_distribution import create_app, db
from cosmetic_distribution.models import Product, User
from settings import TestConfig


class TestLoggedOutUrls(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_class=TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_login_page(self):
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Авторизация', html)
        self.assertIn('Имя пользователя', html)

    def test_unauthorized_client_cant_get_login_required_urls(self):
        urls = [
            '/logout', '/add_product', '/products',
            '/add_customer', '/add_order',
            '/orders', '/orders/1'
        ]
        for url in urls:
            response = self.client.get(url)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 401)
            self.assertIn('Unauthorized', html)


class TestLoggedInUrls(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_class=TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()
        cls.client = cls.app.test_client()
        hashed_password = generate_password_hash('pass')
        user = User(username='test_user', password=hashed_password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    @staticmethod
    def login(client, username, password):
        return client.post('/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    @staticmethod
    def logout(client):
        return client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        response = self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Складские остатки', html)
        response = self.logout(client=self.client)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Авторизация', html)

    def test_authorized_client_get_all_urls(self):
        urls = [
            '/add_product', '/products',
            '/add_customer', '/add_order',
            '/orders'
        ]
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_get_all_products(self):
        data = {
            'title': 'test_product',
            'amount': 3,
            'brand': 'test_brand',
            'wholesale_price': 100,
            'retail_price': 200
        }
        new_products = [Product(**data) for _ in range(5)]
        db.session.add_all(new_products)
        db.session.commit()
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 5)
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        response = self.client.get('/products')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Складские остатки', html)
        self.assertIn('test_product', html)
