from django.test import TestCase, Client
from django.urls import reverse

from .templatetags.store_pagination import get_prev_page_link, get_next_page_link
from store.models import Product, Category, Subcategory

def create_cats(k:int):
    for num in range(k):
        Category.objects.create(
            title=f"Category {num}",
        )

def create_subcats(k:int):
    for cat in Category.objects.all():
        for num in range(k):
            Subcategory.objects.create(
                title=f"{cat.title} Subcategory {num}",
                cat=cat,
            )

def create_products(k:int):
    for num in range(k):
        Product.objects.create(
            price = num+num,
            discount = 15 if num % 4 == 0 else 0,
            title = f"Product {num}",
            description = f"Description {num}",
            article = num,
        )

class TestStorePagination(TestCase):
    def setUp(self):
        create_cats(10)
        create_subcats(10)
        create_products(72)

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