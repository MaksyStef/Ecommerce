from polymorphic.models import PolymorphicModel

from django.db import models
from django.db.models import QuerySet
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from abc import ABCMeta, abstractmethod
import uuid
import re


User = settings.AUTH_USER_MODEL


# Create new Meta class and ABCmodel for future abstractmethods handling
class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class ABCModel(models.Model):
    __metaclass__ = AbstractModelMeta

    class Meta:
        abstract = True


# Models
class AbstractContainer(ABCModel):
    """ Abstract class to define the get_new container function for ForeignKey fields default. """
    @classmethod
    def get_new(cls):
        return cls.objects.create().id



class AbstractProductContainer(AbstractContainer):
    """ Abstract container for products. """
    products = models.ManyToManyField('Product')

    def toggle(self, product):
        if self.products.all().contains(product):
            self.products.remove(product)
            return False
        else:
            self.products.add(product)
            return True

class Favourite(AbstractProductContainer):
    """ Product container for saving products. """
    pass


class Cart(AbstractProductContainer):
    """ Product container for purchasing products. """
    pass

 
class Vote(models.Model):
    """ User vote for a product. """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        editable=False,
        default=None,
    )
    value = models.FloatField(
        editable=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

class AbstractCategory(ABCModel):
    """ 
        Categories ancestor with fields of title, slug and created_at timestamp.
        
        Creates slug on save, orders categories by created_at, return title as representative.
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False,)
    created_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        """ Create slug, created_at and saves object """
        if not self.id:
            created_at = timezone.now()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subcategory(AbstractCategory):
    cat = models.ForeignKey(to='Category', on_delete=models.CASCADE)

    def get_absolute_url(self, class_name:str):
        """ Returns subcategory url of certain Product subclass """
        return f'{reverse("store:products")}/{class_name}/{self.slug}'


class Category(AbstractCategory):
    is_filter = models.BooleanField(default=False)

    def get_subcats(self, ordering:str, subcats: QuerySet) -> QuerySet:
        """ Return all subcats related to Category object if not given Subcategory QuerySet """
        if subcats:
            return subcats.objects.filter(cat_id=self.id).order_by(ordering if ordering else "created_at")
        return Subcategory.objects.filter(cat_id=self.id).order_by(ordering if ordering else "created_at")


class Product(PolymorphicModel):
    """ 
        Product parent model.
    """
    price = models.FloatField(verbose_name="Product price", validators=[MinValueValidator(0)])
    discount = models.IntegerField(
        verbose_name="Discount percent",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    sellable = models.BooleanField(default=True)
    sold = models.PositiveIntegerField(default=0)
    bonus_points = models.PositiveIntegerField(editable=False, blank=True, null=True)
    title = models.CharField(verbose_name="Product title", max_length=255)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False,)
    description = models.TextField(verbose_name="Product description")
    article = models.SmallIntegerField(validators=[MaxValueValidator(999999999999999999), MinValueValidator(0)])
    votes = models.ManyToManyField('Vote')
    subcats = models.ManyToManyField('Subcategory')
    cats = models.ManyToManyField('Category', editable=False)
    in_stock = models.PositiveIntegerField(default=0)
    image_general = models.ImageField(upload_to='store/images/products/general/', null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.id:
            # Get all categories after adding subcategories
            cats = Category.objects.none()
            for subcat in self.subcats.all():
                if subcat.cat not in cats.all():
                    cats = cats.union(Category.objects.filter(id=subcat.cat_id))
            # Remove all categories that doesn't have subcategories in subcats
            for cat in self.cats.all():
                if cat not in cats:
                    self.cats.remove(cat)
            super().save(*args, **kwargs)
            # Add categories in cats
            for cat in cats.all():
                self.cats.add(cat)
        self.bonus_points = (self.price - (self.discount/100 * self.price)) / 5
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def rate(self, rating: int, user: User):
        vote, is_new = self.votes.get_or_create(
            user=user,
            defaults={
                'user': user,
                'value': rating,
            }
        )
        if not is_new:
            vote.value = rating

        vote.save()
        return vote.value

    def get_rating(self):
        """ Returns the rating of product. \n\nPrecision of the fraction is two numbers """
        votes = self.votes.all().values_list('value', flat=True)
        return float(f'{sum(votes) / len(votes):.2f}') if len(votes) > 0 else 0

    def get_personal_rating(self, user: User):
        return self.votes.get(user_id=user.pk).value if user and self.votes.filter(user_id=user.pk).exists() else None

    @classmethod
    def get_images(model):
        images = {}
        for field in [field for field in model._meta.fields if re.match('image_', field.name)]:
            images.update({
                f'{field.name}':field.url if hasattr(field, 'url') else None,
            })
        return images


    def __str__(self):
        return self.title


class ProductChildMixin:
    def get_absolute_url_to_type(self):
        return f"{reverse('store:products')}/{self.__class__.__name__}"

    def get_absolute_url(self):
        return f"{reverse('store:product')}/{self.__class__.__name__}/{self.slug}"
        

class Knife(Product, ProductChildMixin):
    total_length = models.PositiveIntegerField(default=0)
    edge_length = models.PositiveIntegerField(default=0)
    edge_width = models.PositiveIntegerField(default=0)
    image_edge = models.ImageField(upload_to="store/images/products/knives/edge/", null=True, blank=True)
    image_case = models.ImageField(upload_to="store/images/products/knives/case/", null=True, blank=True)
    image_handle = models.ImageField(upload_to="store/images/products/knives/handle/", null=True, blank=True)
    image_guard_and_back = models.ImageField(upload_to="store/images/products/knives/guard_and_back/", null=True, blank=True)
 
class Melee(Product, ProductChildMixin):
    total_length = models.PositiveIntegerField(default=0)
    edge_length = models.PositiveIntegerField(default=0)
    edge_width = models.PositiveIntegerField(default=0)
    spike_thickness = models.PositiveIntegerField(default=0)
    image_edge = models.ImageField(upload_to="store/images/products/melee/edge/", null=True, blank=True)
    image_case = models.ImageField(upload_to="store/images/products/melee/case/", null=True, blank=True)
    image_handle = models.ImageField(upload_to="store/images/products/melee/handle/", null=True, blank=True)
    image_guard_and_back = models.ImageField(upload_to="store/images/products/melee/guard_and_back/", null=True, blank=True)


class Souvenir(Product, ProductChildMixin):
    pass


class Flashlight(Product, ProductChildMixin):
    power = models.PositiveIntegerField(default=0)
    battery_capacity = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    length = models.PositiveIntegerField(default=0)
    thickness = models.PositiveIntegerField(default=0)
    materials = models.PositiveIntegerField(default=0)


class Accompanying(Product, ProductChildMixin):
    pass