from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import (
    Product,
    Supercategory,
    Category,
    Subcategory,
)

class TestHomepageView(TestCase):
    def test_homepage_response(self):
        client = Client()

        response = client.get(reverse('store:homepage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/homepage.html')
        