from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.core.files.uploadedfile import SimpleUploadedFile

from store.models import (
    Product,
    Knife,
    Subcategory,
    Category,
    Favourite,
    Cart,
    Vote
)


User = get_user_model()


# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            first_name='Test',
            last_name='Est',
            email='test@example.com',
            city="City",
            state="State",
            postal_code='123'
        )
        self.category = Category.objects.create(title='Category 1')
        self.subcategory = Subcategory.objects.create(title='Subcategory 1', cat=self.category)
        self.product = Product.objects.create(
            price=10.99,
            discount=20,
            title='Product 1',
            description='Description of Product 1',
            article=123456,
        )
        self.product.subcats.add(self.subcategory)
        self.product.save()
        self.vote = Vote.objects.create(user=self.user, value=5)
        self.product.votes.add(self.vote)
        self.knife = Knife.objects.create(
            price=10.99,
            discount=20,
            title='Knife',
            description='Description of Knife',
            article=1234567,
            total_length = 120,
            edge_length = 100,
            edge_width = 12,
            materials = "Wood, Plastic"
        )

    def test_rate_product(self):
        rating = 4
        self.product.rate(rating, self.user)
        updated_vote = Vote.objects.get(pk=self.vote.pk)
        self.assertEqual(updated_vote.value, rating)

    def test_get_rating(self):
        expected_rating = 5.0
        rating = self.product.get_rating()
        self.assertEqual(rating, expected_rating)

    def test_get_personal_rating(self):
        personal_rating = self.product.get_personal_rating(self.user)
        self.assertEqual(personal_rating, self.vote.value)

    def test_get_article(self):
        expected_article = '000000000000123456'
        article = self.product.get_article()
        self.assertEqual(article, expected_article)

    def test_get_type_cats(self):
        expected_categories = [self.category]
        categories = Product.get_type_cats()
        self.assertCountEqual(categories, expected_categories)

    def test_get_absolute_url(self):
        expected_url = f'/product/{self.product.slug}/'
        url = self.product.get_absolute_url()
        self.assertEqual(url, expected_url)

    def test_polymorphic_queryset(self):
        queryset = Product.objects.all()
        self.assertIn(self.knife, queryset)
    
    def test_product_child_get_absolute_url_to_type(self):
        expected_url = '/products/knife/'
        url = self.knife.get_absolute_url_to_type()
        self.assertEqual(url, expected_url)

    def test_get_properties(self):
        expected_properties = {
            'total length': 120,
            'edge length': 100,
            'edge width': 12,
            'materials': "Wood, Plastic"
        }
        properties = self.knife.get_properties()
        self.assertEqual(properties, expected_properties)


class SubcategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1')
        self.subcategory = Subcategory.objects.create(title='Subcategory 1', cat=self.category)

    def test_get_products(self):
        queryset = Product.objects.all()  # Replace with your Product model
        products = self.subcategory.get_products(queryset=queryset)
        self.assertEqual(products.count(), 0)


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1')
        self.subcategory = Subcategory.objects.create(title='Subcategory 1', cat=self.category)

    def test_get_subcats(self):
        subcats = self.category.get_subcats()
        self.assertEqual(subcats.count(), 1)
        self.assertEqual(subcats.first(), self.subcategory)

    def test_get_products(self):
        queryset = Product.objects.all()
        products = self.category.get_products(queryset=queryset)
        self.assertEqual(products.count(), 0)
