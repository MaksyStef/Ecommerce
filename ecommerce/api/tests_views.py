from django.test import TestCase, Client
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