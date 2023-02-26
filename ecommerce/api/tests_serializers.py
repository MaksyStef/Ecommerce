from django.test import TestCase
from . import serializers
from store.models import Product, Subcategory, Category
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
            article = '000000000000000001',
            in_stock = 10,
        )

        p.rate(4, u)


    def testSerializeOne(self):
        p = Product.objects.all()[0]
        serializer = serializers.ProductSerializer(p)
        self.assertTrue(serializer.data != {})
        print(serializer.data)