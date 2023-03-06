from django.test import TestCase
from . import serializers
from store.models import Product, Subcategory, Category, Knife, Flashlight
from account.models import Account


# Create your tests here.
class StoreSerializerTest(TestCase):
    
    def setUp(self):
        u = Account.objects.create_user(username="testUser A", email="testemail@gmail.com", password="testPassword123")
        p = Product.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Product A',
            description = 'Product A description',
            article = 10,
            in_stock = 10,
        )
        p.rate(4, u)

    def testSerializeOne(self):
        p = Product.objects.all()[0]
        serializer = serializers.ProductSerializer(p)
        self.assertTrue(serializer.data != {})

    def testSerializeMany(self):
        p = Product.objects.all()
        serializer = serializers.ProductSerializer(p, many=True)
        self.assertTrue(serializer.data != {})

    def testSerializeChildClass(self):
        Knife.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Product Knife',
            description = 'Product knife description',
            article = 1,
            in_stock = 10,

            materials = 'afsdsa',
            total_length = 100,
            edge_length = 80,
            edge_width = 14,
        )
        Flashlight.objects.create(
            price = 100,
            discount = 0,
            sellable = True,
            sold = 1,
            title = 'Product Flashlight',
            description = 'Product flashlight description',
            article = 121,
            in_stock = 10,

            materials = 'afsdsa',
            power = 1243,
            battery_capacity = 12,
            width = 100,
            length = 100,
            thickness = 20,
        )
        p = Knife.objects.all()
        serializer = serializers.ProductSerializer(p, many=True)
        self.assertTrue(serializer.data != {})