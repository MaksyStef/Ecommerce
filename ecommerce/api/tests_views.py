from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from . import serializers
from store.models import Product, Subcategory, Category
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
            article = '000000000000000001',
            in_stock = 10,
        )

        p.rate(4, u)

    # def testGet(self):
    #     c = Client()
    #     c.get(reverse('api:'))

    def testRate(self):
        c = Client()
        c.login(username="testUser A", password="testPassword123")
        p = Product.objects.all()[0]
        url = reverse('api:product-rate', None, [p.pk])
        resp = c.put(url, json.dumps({'value': 4}), 'application/json')
        self.assertEqual(resp.status_code, 200, f'Error code: {resp.status_code}')
        print(resp)