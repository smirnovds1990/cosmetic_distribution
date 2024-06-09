import unittest
from werkzeug.security import generate_password_hash

from cosmetic_distribution import create_app, db
from cosmetic_distribution.models import Customer, User
from settings import TestConfig


class TestViewsCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_customer(self):
        new_customer = Customer(name='Иван Иванов')
        db.session.add(new_customer)
        db.session.commit()
        query = Customer.query.all()
        self.assertEqual(len(query), 1)

    def test_login_page(self):
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Авторизация', html)
        self.assertIn('Имя пользователя', html)

    def test_login_logout(self):
        hashed_password = generate_password_hash('pass')
        user = User(username='test_user', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        response = self.client.post(
            '/',
            data={
                'username': 'test_user',
                'password': 'pass'
                },
            follow_redirects=True
        )
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Складские остатки', html)
        response = self.client.get('/logout', follow_redirects=True)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Авторизация', html)
