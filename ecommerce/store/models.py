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
        if self.products.filter(pk=product.pk).exists():
            self.products.remove(product)
            return "remove", None
        else:
            self.products.add(product)
            return "add", product


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
    This is a model for representing abstract categories in Django. It contains the fields title, slug, and created_at.

    title: character field of maximum length 50
    slug: slug field which takes on a unique value using the uuid module each time a new record is created
    created_at: a date-time field set to null by default and not editable once populated
    
    save(): creates a unique slug value, populates created_at with the current timezone, and saves the object.
    str(self): string representation of the object uses the title
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
    
    def get_products(self, model='Product', queryset=None):
        model = globals().get(model)
        if not queryset:
            queryset = model.objects.all()
        return queryset.filter(subcats__in=[self.id])


class Category(AbstractCategory):
    FILTER_TYPES = [
        ('NOT', 'NOT FILTER'),
        ('CBX', 'CHECKBOX FILTER'),
        ('RAN', 'RANGE FILTER'),
    ]
    # is_filter = models.CharField(
    #     max_length  = 100,
    #     choices     = FILTER_TYPES,
    # )
    def get_subcats(self, ordering:str="created_at", subcats:QuerySet=None) -> QuerySet:
        """ Return all subcats related to Category object if not given Subcategory QuerySet """
        if subcats:
            return subcats.objects.filter(cat_id=self.id).order_by(ordering if ordering else "created_at")
        return Subcategory.objects.filter(cat_id=self.id).order_by(ordering if ordering else "created_at")

    def get_products(self, model='Product', queryset=None): # we'll define Product model later, so we use globals() to "predefine" it
        model = globals().get(model)
        if not queryset:
            queryset = model.objects.all()
        return queryset.filter(cats__in=[self.id])


class Product(PolymorphicModel):
    """
    This model contains fields pertinent to a product.

    Fields
    price - A FloatField containing the price of the product. The value must be at least 0.

    discount - An IntegerField containing the percentage discount applied to the product. Its validators ensure that it is between 0 and 100.

    created_at - A DateTimeField denoting when the product was created. It has the auto_now and auto_created attribute set to true.

    sellable - A BooleanField indicating whether the product can still be bought, with a default value of True.

    sold - A PositiveIntegerField indicating how many have been sold, with a default value of 0.

    bonus_points - A PositiveIntegerField indicating the bonus points earned by purchasing the product, which cannot be edited, and defaults to null.

    title - A CharField containing a title string, with a max length of 255.

    slug - A SlugField containing an unique slug, and defaults to an UUID. It is not editable.

    description - A TextField containing a description of the item.

    article - A SmallIntegerField containing a unique identifier representing the article. Its validators ensures it is within the range from 0 to 99999999999999.

    votes - A ManyToManyField, referencing the Vote model.

    subcats - A ManyToManyField, referencing the Subcategory model.

    cats - A ManyToManyField, referencing the Category model, which is not editable.

    in_stock - A PositiveIntegerField indicating the quantity of the product in stock, with a default value of 0.

    image_general - An ImageField containing a general image uploaded to store/images/products/general/, with its default values set to false.

    Implementation Notes
    In order to make sure that the categories are correctly updated after adding subcategories, we use the save() method override. With each save, we then update the cats field which references the Category model.

    The rate() method helps rate on the basis of rating provided by users and adding/updating votes.

    The get_rating() returns the average rating of the product with precision two.

    The get_personal_rating() returns the personal rating of a user associated with the product.

    The get_images() returns a dictionary mapping all the images associated with the product.

    Finally, __str__ overrides the strings representation of the product object.
    """
    price = models.FloatField(verbose_name="Product price", validators=[MinValueValidator(0)])
    discount = models.IntegerField(
        verbose_name="Discount percent",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    created_at = models.DateTimeField(auto_created=True)
    sellable = models.BooleanField(default=True)
    sold = models.PositiveIntegerField(default=0)
    bonus_points = models.PositiveIntegerField(editable=False, blank=True, null=True)
    title = models.CharField(verbose_name="Product title", max_length=255)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False,)
    description = models.TextField(verbose_name="Product description")
    article = models.SmallIntegerField(validators=[MaxValueValidator(999999999999999999), MinValueValidator(0)])
    votes = models.ManyToManyField('Vote', blank=True)
    subcats = models.ManyToManyField('Subcategory', blank=True)
    cats = models.ManyToManyField('Category', editable=False)
    in_stock = models.PositiveIntegerField(default=0)
    image_general = models.ImageField(upload_to='store/images/products/general/', null=True, blank=True)
    rating = models.PositiveIntegerField(default=0, editable=False, blank=True)

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
            # Set rating
            self.rating = self.get_rating()
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
        self.save()
        return vote.value

    def get_rating(self):
        """ Returns the rating of product. \n\nPrecision of the fraction is two numbers """
        votes = self.votes.all().values_list('value', flat=True)
        return float(f'{sum(votes) / len(votes):.2f}') if len(votes) > 0 else 0

    def get_personal_rating(self, user: User):
        return self.votes.get(user_id=user.pk).value if user and self.votes.filter(user_id=user.pk).exists() else None

    @classmethod
    def get_type_cats(model, ordering:str="created_at", **filters):
        """
        Returns a list of all categories included in ManyToManyField by all objects of Product model
        
        Parameters:
        ordering: string; set ordering of queryset
        **filters: set filters for returned categories
        """
        products = model.objects.all()

        # Create an empty set to store unique category objects
        all_cats = set()

        # Loop through each object of Product model
        for product in products:
            # Add all categories of each object to the set
            all_cats |= set(product.cats.all() if not filters else product.cats.filter(**filters))

        # Return the final list of all unique category objects
        return list(all_cats)

    @classmethod
    def get_images(model):
        images = {}
        for field in [field for field in model._meta.fields if re.match('image_', field.name)]:
            images.update({
                f'{field.name}':field.url if hasattr(field, 'url') else None,
            })
        return images
    
    def get_absolute_url(self):
        return reverse('store:product', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ProductChildMixin:
    """
    ProductChildMixin Documentation
    This mixin is used when working with Django models to create an absolute URL to a newly created product.

    Usage:
    Simply inherit from this ProductChildMixin in the model class for which you would like the absolute URL path to be generated.

    Methods
    get_absolute_url_to_type() - This method returns a string of absolute json API url in terms of store products.
    get_absolute_url() - This method returns a string of absolute url of specific product.
    This method requires a slug field in your model.

    """
    @classmethod
    def get_absolute_url_to_type(model):
        return f"{reverse('store:products')}{slugify(model.__name__)}/" # returns url like: /products/class-slug/


class Knife(Product, ProductChildMixin):
    """
    The Knife model is an extension of Product model and also includes the ProductChildMixin.

    Fields

    total_length
    type: PositiveIntegerField
    default value: 0

    edge_length
    type: PositiveIntegerField
    default value: 0

    edge_width
    type: PositiveIntegerField
    default value: 0

    image_edge
    type: ImageField
    upload path: store/images/products/knives/edge/
    nullable: True
    blank: True

    image_case
    type: ImageField
    upload path: store/images/products/knives/case/
    nullable: True
    blank: True

    image_handle
    type: ImageField
    upload path: store/images/products/knives/handle/
    nullable: True
    blank: True

    image_guard_and_back
    type: ImageField
    upload path: store/images/products/knives/guard_and_back/
    nullable: True
    blank: True
    """
    total_length = models.PositiveIntegerField(default=0)
    edge_length = models.PositiveIntegerField(default=0)
    edge_width = models.PositiveIntegerField(default=0)
    image_edge = models.ImageField(upload_to="store/images/products/knives/edge/", null=True, blank=True)
    image_case = models.ImageField(upload_to="store/images/products/knives/case/", null=True, blank=True)
    image_handle = models.ImageField(upload_to="store/images/products/knives/handle/", null=True, blank=True)
    image_guard_and_back = models.ImageField(upload_to="store/images/products/knives/guard_and_back/", null=True, blank=True)
    materials = models.CharField(max_length=99, default="")

    def get_size(self):
        return f"{self.total_length}x{self.edge_width}"

class Melee(Product, ProductChildMixin):
    """
    The Melee model subclassed from the Product and ProductChildMixin models. This model is used to store information related to melee weapons. It contains the following fields:

    total_length : PositiveIntegerField - The total length of the weapon. (default 0)
    edge_length : PositiveIntegerField - The length of the weapon's edge. (default 0)
    edge_width : PositiveIntegerField - The width of the weapon's edge. (default 0)
    edge_thickness : PositiveIntegerField - The thickness of the weapon's edge. (default 0)
    image_edge : ImageField - An image file for the weapon's edge. (upload_to="store/images/products/melee/edge/")
    image_case : ImageField - An image file for the weapon's case. (upload_to="store/images/products/melee/case/")
    image_handle : ImageField - An image file for handle of the weapon. (upload_to="store/images/products/melee/handle/")
    image_guard_and_back : ImageField - An image file for guard and back of the weapon. (upload_to="store/images/products/melee/guard_and_back/")

    """
    total_length = models.PositiveIntegerField(default=0)
    edge_length = models.PositiveIntegerField(default=0)
    edge_width = models.PositiveIntegerField(default=0)
    edge_thickness = models.PositiveIntegerField(default=0)
    image_edge = models.ImageField(upload_to="store/images/products/melee/edge/", null=True, blank=True)
    image_case = models.ImageField(upload_to="store/images/products/melee/case/", null=True, blank=True)
    image_handle = models.ImageField(upload_to="store/images/products/melee/handle/", null=True, blank=True)
    image_guard_and_back = models.ImageField(upload_to="store/images/products/melee/guard_and_back/", null=True, blank=True)
    materials = models.CharField(max_length=99, default="")

    def get_size(self):
        return f"{self.total_length}x{self.edge_width} ({self.edge_thickness})"


class Souvenir(Product, ProductChildMixin):
    """
    This is a class that inherits from the base Product class and includes the ProductChildMixin, making it part of a product hierarchy.

    Class Details:

    Name: Souvenir
    Inherits from: Product and ProductChildMixin
    Functions: None
    Usage: This class is used as part of a product hierarchy to provide additional functionality.
    """
    materials = models.CharField(max_length=99, default="", null=True)


class Flashlight(Product, ProductChildMixin):
    """
    Fields
    power - PositiveIntegerField to store the power of the product. Default value is 0.
    battery_capacity - PositiveIntegerField to store the battery capacity of the product. Default value is 0.
    width - PositiveIntegerField to store the width of the product. Default value is 0.
    length - PositiveIntegerField to store the length of the product. Default value is 0.
    thickness - PositiveIntegerField to store the thickness of the product. Default value is 0.
    materials - PositiveIntegerField to store the materials used in the product. Default value is 0.

    Validators
    All fields must be of type PositiveIntegerField.
    All fields have a default value of 0.

    Methods
    get_product_dimensions() - Returns a tuple containing the width, length, and thickness of the product.
    get_product_materials() - Returns a list of strings containing the names of the materials used in the product.
    get_product_power() - Returns an integer representing the power of the product.
    """
    power = models.PositiveIntegerField(default=0)
    battery_capacity = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    length = models.PositiveIntegerField(default=0)
    thickness = models.PositiveIntegerField(default=0)
    materials = models.CharField(max_length=99, default="")


class Accompanying(Product, ProductChildMixin):
    """
    This is a class that inherits from the base Product class and includes the ProductChildMixin, making it part of a product hierarchy.

    Class Details:

    Name: Accompanying
    Inherits from: Product and ProductChildMixin
    Functions: None
    Usage: This class is used as part of a product hierarchy to provide additional functionality.
    """
    pass