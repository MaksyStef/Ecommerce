from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from store.models import Favourite, Cart
from .managers import AccountManager


# Create your models here.
class Account(AbstractBaseUser, PermissionsMixin): # Sometimes need to remove PermissionsMixin, migrate and then put it back
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    favourite = models.OneToOneField(
        Favourite,
        verbose_name=("Favourite products"),
        on_delete=models.CASCADE,
        unique=True,
        default=Favourite.get_new,
    )
    cart = models.OneToOneField(
        Cart,
        verbose_name=("Products in cart"),
        on_delete=models.CASCADE,
        unique=True,
        default=Cart.get_new,
    )
    bonus_points = models.PositiveIntegerField(default=0, editable=False, blank=True)

    objects = AccountManager()


    def get_cart_count(self):
        return self.cart.products.all().count()

    def get_favourite_count(self):
        return self.favourite.products.all().count()

    def get_payment_price(self):
        return sum(self.cart.products.all().values_list('price', flat=True))