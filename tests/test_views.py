import unittest
from werkzeug.security import generate_password_hash

from cosmetic_distribution import create_app, db
from cosmetic_distribution.models import Customer, Order, Product, User
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
        self.login(
            client=self.client,
            username='test_user',
            password='pass'
        )

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

    def test_add_customer(self):
        all_customers = Customer.query.all()
        self.assertEqual(len(all_customers), 0)
        self.client.post(
            '/add_customer',
            data=dict(name='Иван Иванов'),
            follow_redirects=True
        )
        all_customers = Customer.query.all()
        self.assertEqual(len(all_customers), 1)
        self.assertEqual(all_customers[0].name, 'Иван Иванов')

    def test_add_product(self):
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 0)
        self.client.post(
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
        all_products = Product.query.all()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0].title, 'New_test_product')
        self.assertEqual(all_products[0].amount, 5)

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
        self.assertEqual(all_products[0].amount, 3)
        self.client.post(
            '/delete_product/1',
            follow_redirects=True,
            data={'_method': 'DELETE'}
        )
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
        all_orders = Order.query.all()
        self.assertEqual(len(all_orders), 0)
        self.client.post(
            '/add_order',
            follow_redirects=True,
            data={
                'customer': str(test_customer.id),
                'products-0-products': str(test_product.id),
                'products-0-quantity': '2',
                'products-0-price': '200'
            }
        )
        all_orders = Order.query.all()
        self.assertEqual(len(all_orders), 1)

    def test_get_all_orders(self):
        test_customer = Customer(name='test_customer')
        test_product = Product(
            title='test_product',
            amount=10,
            brand='Test_brand',
            wholesale_price=100,
            retail_price=200
        )
        db.session.add_all([test_customer, test_product])
        db.session.commit()
        data = {
            'customer': str(test_customer.id),
            'products-0-products': str(test_product.id),
            'products-0-quantity': '1',
            'products-0-price': '200'
        }
        for _ in range(6):
            self.client.post(
                '/add_order',
                follow_redirects=True,
                data=data
            )
        response = self.client.get('/orders')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Заказы', html)
        product_amount = Product.query.filter_by(
            title='test_product'
        ).first_or_404()
        self.assertEqual(product_amount.amount, 4)

    def test_get_and_delete_order(self):
        test_customer = Customer(name='test_customer')
        test_product = Product(
            title='test_product',
            amount=10,
            brand='Test_brand',
            wholesale_price=100,
            retail_price=200
        )
        db.session.add_all([test_customer, test_product])
        db.session.commit()
        data = {
            'customer': str(test_customer.id),
            'products-0-products': str(test_product.id),
            'products-0-quantity': '1',
            'products-0-price': '200'
        }
        self.client.post(
            '/add_order',
            follow_redirects=True,
            data=data
        )
        response = self.client.get('/orders/1')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Заказ от', html)
        response = self.client.get('/orders/2')
        self.assertEqual(response.status_code, 404)
        response = self.client.post(
            '/delete_order/1',
            follow_redirects=True,
            data={'_method': 'DELETE'}
        )
        html = response.get_data(as_text=True)
        all_orders = Order.query.all()
        self.assertIn('Заказы', html)
        self.assertEqual(len(all_orders), 0)
