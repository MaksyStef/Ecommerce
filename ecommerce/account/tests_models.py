from django.test import TestCase, Client
from .models import Account
from store.models import Product, Cart, Favourite


# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        self.account = Account.objects.create(username='testuser', email='test@example.com', first_name='John', last_name='Doe')
        self.product1 = Product.objects.create(
            title="Product 1",
            description="Description of Product 1",
            price=10.99,
            discount=0,
            article=1234,
        )
        self.product2 = Product.objects.create(
            title="Product 2",
            description="Description of Product 2",
            price=9.99,
            discount=10,
            article=12345,
        )
        self.product3 = Product.objects.create(
            title="Product 3",
            description="Description of Product 3",
            price=8.99,
            discount=20,
            article=123456,
        )

    def test_get_cart_count(self):
        cart = self.account.cart
        cart.bulk_toggle(self.product1, self.product2, self.product3)
        cart_count = self.account.get_cart_count()
        self.assertEqual(cart_count, 3)

    def test_get_favourite_count(self):
        favourite = self.account.favourite
        favourite.bulk_toggle(self.product1, self.product2, self.product3)
        favourite_count = self.account.get_favourite_count()
        self.assertEqual(favourite_count, 3)

    def test_get_payment_price(self):
        cart = self.account.cart
        cart.toggle(self.product1)
        payment_price = self.account.get_payment_price()
        self.assertEqual(payment_price, 10.99)  # Replace 0 with the expected payment price

    def test_username_field(self):
        self.assertEqual(self.account.USERNAME_FIELD, 'username')

    def test_required_fields(self):
        self.assertEqual(self.account.REQUIRED_FIELDS, ['email'])