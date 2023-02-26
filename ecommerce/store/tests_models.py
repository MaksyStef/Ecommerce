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
)


User = get_user_model()


# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        cat = Category.objects.create(title='Сategory 1')
        subcat = Subcategory.objects.create(title='Subcategory 1', cat=cat)

        Product.objects.create(
            title       = 'Product 1',
            price       = 100,
            discount    = 10,
            sellable    = True,
            description = 'Test product description',
            article     = '0000128411111111',
            in_stock    = 10,
        )

        User.objects.create_user(
            username = "Testuser",
            email    = "test@gmail.com",
            password = "testpassword123"
        )

    def test_toggle_favourite(self):
        product = Product.objects.all().get()
        user = User.objects.all().get()

        user.favourite.toggle(product)
        fav = Favourite.objects.create()
        fav.products.add(product)
        fav.save()
        self.assertEqual(
            fav.products.all().get(),
            user.favourite.products.all().get(),
            f"""
Favourite products: {fav.products.all()}
User fav products: {user.favourite.products.all()}
            """
        )
        fav.products.remove(product)
        user.favourite.toggle(product)
        self.assertEqual(
            fav.products.all().exists(),
            user.favourite.products.all().exists(),
            f"""
Favourite products: {fav.products.all()}
User fav products:  {user.favourite.products.all()}
            """
        )

    def test_toggle_cart(self):
        product = Product.objects.all().get()
        user = User.objects.all().get()

        user.cart.toggle(product)
        cart = Cart.objects.create()
        cart.products.add(product)
        cart.save()
        self.assertEqual(
            cart.products.all().get(),
            user.cart.products.all().get(),
            f"""
Cart products:      {cart.products.all()}
User cart products: {user.cart.products.all()}
            """
        )
        cart.products.remove(product)
        user.cart.toggle(product)
        self.assertEqual(
            cart.products.all().exists(),
            user.cart.products.all().exists(),
            f"""
Cart products:      {cart.products.all()}
User cart products: {user.cart.products.all()}
            """
        )

    def test_rating(self):
        product = Product.objects.all().get()
        user = User.objects.all().get()

        rating = 2
        product.rate(rating, user)
        self.assertEqual(
            product.get_rating(),
            rating,
            f"""
Rating:         {rating}
Product rating: {product.get_rating()}
            """
        )
        self.assertEqual(
            product.get_personal_rating(user),
            rating,
            f"""
Rating:          {rating}
Personal rating: {product.get_personal_rating(user)}
            """
        )

    def test_cats_autofill(self):
        product = Product.objects.all().get()

        product.subcats.add(Subcategory.objects.all().get())
        product.save()
        self.assertTrue(
            product.cats.filter(id=Category.objects.all().get().pk).exists(),
            f"""
Product cats:    {product.cats.all()}
Product subcats: {product.subcats.all()}
            """
        )
        product.subcats.remove(Subcategory.objects.all().get())
        product.save()
        self.assertTrue(
            not product.cats.filter(id=Category.objects.all().get().pk).exists(),
            f"""
Product cats:    {product.cats.all()}
Product subcats: {product.subcats.all()}
            """
        )
    
    def test_products_polymorphism(self):
        knife = Knife.objects.create(
            title        = 'Knife 1',
            price        = 100,
            discount     = 10,
            sellable     = True,
            description  = 'Test knife description',
            article      = '11111284',
            in_stock     = 10,
            total_length = 100,
            edge_length  = 90,
            edge_width   = 10,
        )
        self.assertIn(
            knife, 
            Product.objects.all(),
            f"""Products: {Product.objects.all()}"""
        )
    
    def test_products_get_images(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        knife = Knife.objects.create (
            title        = 'Knife 1',
            price        = 100,
            discount     = 10,
            sellable     = True,
            description  = 'Test knife description',
            article      = '11111284',
            in_stock     = 10,
            total_length = 100,
            edge_length  = 90,
            edge_width   = 10,
        )
        self.assertIn(
            '/store/images/products/general/',
            knife.get_images(),
            f"""
Knife urls: {knife.get_images()}
Expected  : /store/images/products/general/
             """
        )