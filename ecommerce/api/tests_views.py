from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from store.models import Product
from unittest.mock import patch, MagicMock
from .serializers import ProductSerializer
from store.models import Order

User = get_user_model()


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Product A',
            description = 'Product A description',
            article = 10,
            in_stock = 10,
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            city='New York',
            state='NY',
            postal_code='12345',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_suggestions(self):
        url = reverse('api:product-suggestions', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_buy_altogether(self):
        url = reverse('api:product-buy_altogether', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rate_product(self):
        url = reverse('api:product-rate', args=[self.product.id])
        data = {'value': 5}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'success')
        self.assertEqual(response.data['value'], 5)

    def test_toggle_favourite(self):
        url = reverse('api:product-toggle_favourite', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'add')
        self.assertEqual(response.data['product_pk'], 1)
        response = self.client.post(url)
        self.assertEqual(response.data['result'], 'remove')
        self.assertEqual(response.data['product_pk'], None)

    def test_toggle_cart(self):
        url = reverse('api:product-toggle_cart', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'add')
        self.assertEqual(response.data['order_pk'], 1)
        response = self.client.post(url)
        self.assertEqual(response.data['result'], 'remove')
        self.assertEqual(response.data['order_pk'], None)

    def test_search(self):
        test_product = Product.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Similar Product Name',
            description = 'Similar description',
            article = 10,
            in_stock = 10,
        )
        query_string = 'Similar Name'
        url = reverse('api:product-search', kwargs={'query_string': query_string})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = HttpRequest()
        request.user = self.user
        serializer = ProductSerializer([test_product,], many=True, context={'request': request})
        self.assertEqual(serializer.data, response.data['results'])


class OrderViewSetTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
                price=11.5,
                discount=10,
                sold=1,
                title="Test Product",
                description=f"Product number 1",
                article=20,
                in_stock=10,
            )
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            city='Berlin',
            state='Brandenburh',
            postal_code='10315',
        )
        self.user.cart.toggle(self.product)
        self.client.force_authenticate(user=self.user)

    def test_create_paypal_order(self):
        url = reverse('api:order-create_paypal_order')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)

    @patch('core.settings.PAYPAL_CLIENT.execute')
    def test_capture_paypal_order(self, mock_execute):
        order = self.user.cart.orders.first()
        url = reverse('api:order-capture_paypal_order')

        # Mock the execute method to return a response with the completed status
        mock_response = MagicMock()
        mock_response.result.status = 'COMPLETED'
        mock_response.result.id = '123456789'
        mock_execute.return_value = mock_response

        response = self.client.post(url, {'order_id': 'dummy_order_id'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertTrue(order.is_paid)
        self.assertEqual(order.capture_id, '123456789')