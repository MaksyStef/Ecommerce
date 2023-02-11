from django.test import TestCase, Client
from django.urls import reverse

from .templatetags.store_pagination import get_prev_page_link, get_next_page_link
from api.tests import create_products, create_supercats, create_cats, create_subcats
from store.models import Product

class TestStorePagination(TestCase):
    def setUp(self):
        create_supercats()
        create_cats(10)
        create_subcats(10)
        create_products(10)

    def test_get_prev_page_link(self):
        c = Client()

        url = reverse('store:products')+'?page=2'
        response = c.get(url)
        result = get_prev_page_link(response.context, url)

        self.assertTrue(
            result == reverse('store:products')+'?page=1' or 
            result == reverse('store:products'),
            f'''
\n\nRESULT: {result}
\nEXPECTED: {reverse('store:products')+'?page=1'} or {reverse('store:products')}
             '''
        )

    def test_get_prev_page_link_with_parameters(self):
        c = Client()

        url = reverse('store:products')+'?count=76&ordering=-price&page=2'
        response = c.get(url)
        result = get_prev_page_link(response.context, url)

        self.assertTrue(
            result == reverse('store:products')+'?count=76&ordering=-price&page=1', 
            f'''
\nRESULT: {result}
EXPECTED: {reverse('store:products')+'?page=1'} or {reverse('store:products')}
\nPAGES COUNT: {response.context.get('page_obj').paginator.page_range}'''
        )

    def test_get_next_page_link_without_parameters(self):
        c = Client()

        url = reverse('store:products')
        response = c.get(url)
        result = get_next_page_link(response.context, url)

        self.assertTrue(
            result == '/products/?page=2',
            f'''
\nRESULT: {result}
EXPECTED: /products/?page=2
\nPAGES COUNT: {response.context.get('page_obj').paginator.page_range}
TOTAL PRODUCTS NUMBER: {Product.objects.all().count()}'''
        )
    
    def test_get_next_page_link_with_page_parameter(self):
        c = Client()

        url = reverse('store:products') + '?page=2'
        response = c.get(url)
        result = get_next_page_link(response.context, url)
        self.assertTrue(
            result == '/products/?page=3',
            f'''
\nRESULT: {result}
EXPECTED: /products/?page=3
\nPAGES COUNT: {response.context.get('page_obj').paginator.page_range}
TOTAL PRODUCTS NUMBER: {Product.objects.all().count()}'''
        )

    def test_get_next_page_link_with_many_parameters(self):
        c = Client()

        url = reverse('store:products') + '?ordering=discount&count=86&page=2'
        response = c.get(url)
        result = get_next_page_link(response.context, url)
        self.assertTrue(
            result == '/products/?ordering=discount&count=86&page=3',
            f'''
\nRESULT: {result}
EXPECTED: /products/?page=3
\nPAGES COUNT: {response.context.get('page_obj').paginator.page_range}
TOTAL PRODUCTS NUMBER: {Product.objects.all().count()}'''
        )