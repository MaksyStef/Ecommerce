from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate
from . import serializers
from store.models import Product, Flashlight, Knife, Subcategory, Category
from account.models import Account

import json


# Create your tests here.
class ProductViewSetTest(TestCase):
    
    def setUp(self):
        u = Account.objects.create_user(username="testUser A", email="testemail@gmail.com", password="testPassword123")
        p = Product.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Product A',
            description = 'Product A description',
            article = 1,
            in_stock = 10,
        )
        p.rate(4, u)
        self.client = Client()

    def testToggle(self):
        c = self.client
        u = Account.objects.all()[0]
        c.login(username="testUser A", password="testPassword123")
        p = Product.objects.all()[0]
        url = reverse('api:product-toggle_cart', None, [p.pk])
        resp = c.post(url, secure=False)
        self.assertEqual(resp.status_code, 200, f'Error code: {resp.status_code}')
        self.assertTrue(u.cart.products.all().contains(p), f"Cart contains: {u.cart.products.all()}, must cantain Product A")
        resp = c.post(url, secure=False)
        self.assertFalse(u.cart.products.all().contains(p), f"Cart contains: {u.cart.products.all()}, must be empty")

    def testChildViewSet(self):
        c = self.client
        Flashlight.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Product B',
            description = 'Product B description',
            article = 1,
            in_stock = 10,

            power = 100,
            battery_capacity = 10,
            width = 10,
            length = 10,
            thickness = 10,
            materials = "Material A"
        )
        resp_f = c.get('/api/flashlight/').json()['results']
        resp_p = c.get('/api/product/').json()['results']
        self.assertTrue(resp_f != resp_p)

    def testQueryRequests(self):
        for num in range(5):
            Category.objects.create(title=f"Cat{num}")
            Product.objects.create(
                price=11.5+num,
                discount=10 if num % 3 == 0 else 0,
                sold=num,
                title=f"Cat{num}",
                description=f"Product number {num}",
                article=num**num,
                in_stock=10*num,
            )
        for cat in Category.objects.all():
            for num in range(5):
                s = Subcategory.objects.create(
                    title=f"Subcar{num} {cat.title}",
                    cat=cat,
                )
        
        for index, product in enumerate(Product.objects.all()):
            if index % 2:
                product.subcats.add(Subcategory.objects.all()[index])

        c = self.client

        resp = c.get('/api/product/?price_gap=14_20')
        dummy_request = HttpRequest()
        dummy_request.method = 'GET'
        dummy_request.path = '/'
        dummy_request.META['SERVER_NAME'] = 'localhost'
        dummy_request.META['SERVER_PORT'] = '8000'
        dummy_request.META['HTTP_AUTHORIZATION'] = 'Bearer your_token_here'
        dummy_request.META['HTTP_ACCEPT'] = 'application/json'
        dummy_request.META['CONTENT_TYPE'] = 'application/json'
        dummy_request.user = Account.objects.all().get()
        expected = serializers.ProductSerializer(Product.objects.filter(price__gte=14, price__lte=20), many=True, context={'request': dummy_request}).data
        self.assertEqual(expected, resp.json()['results'], f"\n\nExpected: {expected}\nResponse: {resp}")