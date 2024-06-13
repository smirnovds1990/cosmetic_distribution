import unittest
from werkzeug.security import generate_password_hash

from cosmetic_distribution import create_app, db
from cosmetic_distribution.models import Customer, Product, User
from settings import TestConfig


class TestViewsCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        hashed_password = generate_password_hash('pass')
        user = User(username='test_user', password=hashed_password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def login(client, username, password):
        return client.post('/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    @staticmethod
    def logout(client):
        return client.get('/logout', follow_redirects=True)

    def test_login_page(self):
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Авторизация', html)
        self.assertIn('Имя пользователя', html)

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

    def test_add_customer(self):
        all_customers = Customer.query.all()
        self.assertEqual(len(all_customers), 0)
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        response = self.client.post(
            '/add_customer',
            data=dict(name='Иван Иванов'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        all_customers = Customer.query.all()
        self.assertEqual(len(all_customers), 1)
        self.assertEqual(all_customers[0].name, 'Иван Иванов')

    def test_add_product(self):
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 0)
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        response = self.client.post(
            '/add_product',
            data=dict(
                title='New_test_product',
                amount=5,
                brand='Test_brand',
                wholesale_price=100,
                retail_price=200
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0].title, 'New_test_product')
        self.assertEqual(all_products[0].amount, 5)

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

    def test_delete_product(self):
        data = {
            'title': 'test_product',
            'amount': 3,
            'brand': 'test_brand',
            'wholesale_price': 100,
            'retail_price': 200
        }
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0].id, 1)
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        response = self.client.post(
            '/delete_product/1',
            follow_redirects=True,
            data={'_method': 'DELETE'}
        )
        self.assertEqual(response.status_code, 200)
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0].id, 1)
        self.assertEqual(all_products[0].amount, 0)

    def test_add_order(self):
        test_customer = Customer(name='test_customer')
        test_product = Product(
            title='test_product',
            amount=5,
            brand='Test_brand',
            wholesale_price=100,
            retail_price=200
        )
        db.session.add_all([test_customer, test_product])
        db.session.commit()
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )
        response = self.client.post(
            '/add_order',
            follow_redirects=True,
            data={
                'customer': str(test_customer.id),
                'products-0-products': str(test_product.id),
                'products-0-quantity': '2',
                'products-0-price': '200'
            }
        )
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Заказы', html)
        self.assertIn('test_product', html)
