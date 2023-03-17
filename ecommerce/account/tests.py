from django.test import TestCase, Client
from .models import Account
from store.models import Product


# Create your tests here.
class AccountTest(TestCase):

    def setUp(self):
        self.client = Client
        self.account = Account.objects.create_user(username='test', email='test@example.com', password='testUser123')
    
    def testToggle(self):
        p = Product.objects.create(
            title       = 'Product 1',
            price       = 100,
            discount    = 10,
            sellable    = True,
            description = 'Test product description',
            article     = '0000128411111111',
            in_stock    = 10,
        )
        self.account.cart.toggle(p)
        self.assertTrue(self.account.cart.products.all().contains(p))
        self.account.cart.toggle(p)
        self.assertFalse(self.account.cart.products.all().contains(p))


class ViewTest(TestCase):
     
    def setUp(self):
        self.client = Client()
    
    def signViewTest(self):
        c = self.client
        resp = c.get('/account/sign/')
        self.assertEqual(resp.status_code, 200)
        resp = c.post(path='/account/sign?username=asd&email=test@example.com&password=testUser123&confirmation=testUser123&action=register', follow=True)
        self.assertEqual(resp.status_code, 200)