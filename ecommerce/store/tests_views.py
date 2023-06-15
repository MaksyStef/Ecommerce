from django.test import TestCase, Client, RequestFactory
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import (
    Product,
    Category,
    Subcategory,
)
from .views import *


User = get_user_model()


class HomepageViewTestCase(TestCase):
    def test_homepage_response(self):
        client = Client()

        response = client.get(reverse('store:homepage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/homepage.html')


class NewslettersViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_sign_action(self):
        request = self.factory.post('/newsletters/', {'action': 'sign', 'email': 'test@example.com'})
        response = NewslettersView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'success')

    def test_post_unsign_action(self):
        request = self.factory.post('/newsletters/', {'action': 'unsign', 'email': 'test@example.com'})
        response = NewslettersView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'success')

    def test_post_invalid_action(self):
        request = self.factory.post('/newsletters/', {'action': 'invalid', 'email': 'test@example.com'})
        response = NewslettersView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'success')


class ProductsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_context_data(self):
        category = Category.objects.create(title='Category 1')
        product1 = Product.objects.create(title='Product 1', article=421, price=10, discount=0)
        product1.cats.add(category)
        product2 = Product.objects.create(title='Product 2', article=12421, price=20, discount=0)
        product2.cats.add(category)

        request = self.factory.get('/products/')
        view = ProductsView.as_view(template_name='store/products.html', model=Product)

        response = view(request)

        self.assertIsInstance(response, TemplateResponse)
        context = response.context_data
        self.assertEqual(context['prods_cat'], 'Product')
        self.assertEqual(list(context['filter_cats']), [category])
        self.assertEqual(context['max_price'], 21)
        self.assertEqual(context['min_price'], 10)
        self.assertEqual(context['api_url'], '/api/product/')
        expected_orderings = {
            '-created_at': "Newer",
            'created_at': "Older",
            '-price': "Higher price",
            'price': "Lower price",
            '-rating': "Higher rating",
            'rating': "Lower rating",
            '-sold': "Most popular",
            'sold': "Least popular",
        }
        self.assertEqual(context['orderings'], expected_orderings)


class CertainProductsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        category = Category.objects.create(title='Category 1')
        product1 = Product.objects.create(title='Product 1', article=421, price=10, discount=0)
        product1.cats.add(category)
        product2 = Product.objects.create(title='Product 2', article=12421, price=20, discount=0)
        product2.cats.add(category)
        request = self.factory.get('/products/knife/')
        view = CertainProductsView.as_view(template_name='store/products.html', model=Product)
        response = view(request, product_type='knife')
        self.assertEqual(response.status_code, 200)


    def test_get_range_filters(self):
        product1 = Knife.objects.create(title='Product 1', article=421, price=10, discount=0, rating=4, in_stock=5, total_length=10)
        product2 = Knife.objects.create(title='Product 2', article=12421, price=20, discount=0, rating=3, in_stock=10, total_length=20)
        request = self.factory.get('/products/knife/')
        view = CertainProductsView()
        view.model = Knife

        range_filters = view.get_range_filters()

        expected_filter = {
            'title': 'total length',
            'param_name': 'total_length_gap',
            'max': 20,
            'min': 10
        }
        self.assertIn(expected_filter, range_filters)

    def test_get_context_data(self):
        category = Category.objects.create(title='Category 1')
        product1 = Knife.objects.create(title='Product 1', article=421, price=10, discount=0)
        product1.cats.add(category)
        product2 = Knife.objects.create(title='Product 2', article=12421, price=20, discount=0)
        product2.cats.add(category)

        request = self.factory.get('/products/knife/')
        view = CertainProductsView()
        view.model = Knife

        context = view.get_context_data()

        self.assertEqual(context['supercategory'], Knife)
        self.assertEqual(context['supercategory_title'], 'Knife')
        self.assertEqual(list(context['filter_cats']), [category])


class ProductViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_context_data(self):
        category = Category.objects.create(title='Category 1')
        product = Knife.objects.create(title='Product 1', article=421, price=10, discount=0)
        product.cats.add(category)

        request = self.factory.get('/product/product-1/')
        request.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        view = ProductView.as_view(template_name='store/product.html', model=Knife)
        view.request = request

        response = view(request, slug='product-1')
        context = response.context_data

        self.assertEqual(context['supercat']['name'], 'Knife')
        self.assertEqual(context['supercat']['url'], '/products/knife/')
        self.assertIsNone(context['personal_rating'])
        self.assertFalse(context['in_fav'])
        self.assertFalse(context['in_cart'])
        self.assertIsNone(context['manufacturer'])
        self.assertIsNone(context['series'])
        self.assertEqual(len(context['cats']), 1)
        self.assertEqual(context['cats'][0][0], 'Category 1')
        self.assertEqual(list(context['cats'][0][1]), [])
        self.assertEqual(list(context['properties']), ['materials', 'total length', 'edge length', 'edge width'])


class SearchProductViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_context_data(self):
        category = Category.objects.create(title='Category 1')
        product1 = Product.objects.create(title='Product 1', article=421, price=10, discount=0)
        product2 = Product.objects.create(title='Product 2', article=12421, price=20, discount=0)
        product1.cats.add(category)
        product2.cats.add(category)

        request = self.factory.get('/search/product')
        view = SearchProductView.as_view(template_name='store/products.html', model=Product)
        view.request = request

        response = view(request, query_string='product')
        context = response.context_data

        self.assertEqual(context['api_url'], '/api/product/search/product')


class CartViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_view_with_authenticated_user(self):
        request = self.factory.get(reverse('store:cart'))
        request.user = self.user

        response = CartView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(request.user.is_authenticated)

    def test_view_with_anonymous_user(self):
        request = self.factory.get(reverse('store:cart'))
        request.user = AnonymousUser()

        response = CartView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(request.user.is_authenticated)


class FavouriteViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_get_context_data_authenticated(self):
        product1 = Product.objects.create(title='Product 1', article=421, price=10, discount=0)
        product2 = Product.objects.create(title='Product 2', article=12421, price=20, discount=0)
        favourite = self.user.favourite
        favourite.products.add(product1, product2)

        request = self.factory.get('/favourite/')
        request.user = self.user
        view = FavouriteView.as_view()
        view.request = request

        response = view(request)
        context = response.context_data

        self.assertEqual(context['container_name'], 'favourite')
        self.assertEqual(context['in_container'], 2)
        self.assertQuerysetEqual(context['products'], [product1, product2])

    def test_get_context_data_unauthenticated(self):
        request = self.factory.get('/favourite/')
        request.user = AnonymousUser()
        view = FavouriteView.as_view()
        view.request = request

        response = view(request)

        self.assertEqual(response.status_code, 200)
