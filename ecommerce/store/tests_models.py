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
            f"""Favourite products: {fav.products.all()} \nUser fav products: {user.favourite.products.all()}"""
        )
        fav.products.remove(product)
        user.favourite.toggle(product)
        self.assertEqual(
            fav.products.all().exists(),
            user.favourite.products.all().exists(),
            f"""Favourite products: {fav.products.all()} \nUser fav products:  {user.favourite.products.all()}"""
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
            f"""Cart products: {cart.products.all()} \nUser cart products: {user.cart.products.all()}"""
        )
        cart.products.remove(product)
        user.cart.toggle(product)
        self.assertEqual(
            cart.products.all().exists(),
            user.cart.products.all().exists(),
            f"""Cart products: {cart.products.all()} \nUser cart products: {user.cart.products.all()}"""
        )

    def test_rating(self):
        product = Product.objects.all().get()
        user = User.objects.all().get()

        rating = 2
        product.rate(rating, user)
        self.assertEqual(
            product.get_rating(),
            rating,
            f"""Rating: {rating} \nProduct rating: {product.get_rating()}"""
        )
        self.assertEqual(
            product.get_personal_rating(user),
            rating,
            f"""Rating: {rating} \nPersonal rating: {product.get_personal_rating(user)}"""
        )

    def test_cats_autofill(self):
        product = Product.objects.all().get()

        product.subcats.add(Subcategory.objects.all().get())
        product.save()
        self.assertTrue(
            product.cats.filter(id=Category.objects.all().get().pk).exists(),
            f"""Product cats: {product.cats.all()} \nProduct subcats: {product.subcats.all()}"""
        )
        product.subcats.remove(Subcategory.objects.all().get())
        product.save()
        self.assertTrue(
            not product.cats.filter(id=Category.objects.all().get().pk).exists(),
            f"""Product cats: {product.cats.all()} \nProduct subcats: {product.subcats.all()}"""
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
        self.assertEqual(
            {'image_general': None, 'image_edge': None, 'image_case': None, 'image_handle': None, 'image_guard_and_back': None},
            knife.get_images(),
            f"""Knife urls: {knife.get_images()} \nExpected: /store/images/products/general/"""
        )
    
    def test_children_url_to_type(self):
        self.assertEqual(
            Knife.get_absolute_url_to_type(),
            '/products/knife/',
            Knife.get_absolute_url_to_type(),
        )

    def test_get_cats(self):
        c = Category.objects.all().get()
        s = Subcategory.objects.all().get()
        p = Product.objects.all().get()
        p.subcats.add(s)
        p.save()
        res = p.get_type_cats()
        self.assertIn(c, res, f"Expected list of Categories, got: {res}")

class CategoryTestCase(TestCase):

    def setUp(self):
        Product.objects.create(
            title       = 'Product 1',
            price       = 100,
            discount    = 10,
            sellable    = True,
            description = 'Test product description',
            article     = '0000128411111111',
            in_stock    = 10,
        )
        cat = Category.objects.create(title='Cat1')
        for n in range(1, 11):
            Subcategory.objects.create(
                title=f"Subcat{n} of {cat.title}",
                cat = cat,
            )
        self.cat = cat
    
    def testCreate(self):
        prev = ...
        for i, subcat in enumerate(Subcategory.objects.all()):
            if i > 0:
                self.assertGreater(subcat.created_at.datetime(), prev.created_at.datetime(), f"Must be Subcat > Prev, but {subcat.created_at} not greater than {prev.created_at}")
            prev = subcat
        
    def testGetProducts(self):
        p = Product.objects.first()
        s = Subcategory.objects.first()
        p.subcats.add(s)
        p.save()
        self.assertEqual(s.get_products().count(), 1, f"Subcat: {s}")