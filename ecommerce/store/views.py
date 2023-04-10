from django.db.models import PositiveIntegerField
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.utils.text import slugify
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)
from django.views.generic.base import (
    ContextMixin,
)
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator

from store.utils import newsletter
from store.models import (
    Product,
    Knife,
    Subcategory,
    Category,
)

from api.serializers import ProductSerializer
import json


# Mixins


# Class Based Views
class HomepageView(TemplateView, ContextMixin):
    template_name = "store/homepage.html"


class NewslettersView(View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'sign':
            newsletter.sign(request.GET.get('email'))
        elif request.POST.get('action') == 'unsign':
            newsletter.unsign(request.GET.get('email'))
        return HttpResponse('success')


class ProductsView(TemplateView):
    template_name = 'store/products.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'prods_cat': self.model.__name__,
            'filter_cats': Category.objects.all(),
            'max_price': int(self.model.objects.all().order_by('-price')[0].price)+1 if self.model.objects.all().count() > 0 else None,
            'min_price': int(self.model.objects.all().order_by('price')[0].price)    if self.model.objects.all().count() > 0 else None,
            'api_url': f'/api/{slugify(self.model.__name__)}/', # Set API url depending on self.model
            'orderings': {
                '-created_at': "Newer",
                'created_at': "Older",
                '-price': "Higher price",
                'price': "Lower price",
                '-rating': "Higher rating",
                'rating': "Lower rating",
                '-sold': "Most popular",
                'sold': "Least popular",
            }
        })
        return context
    

class CertainProductsView(ProductsView):

    def get(self, request, product_type, *args, **kwargs):
        subs = list(filter(lambda cls: slugify(cls.__name__) == product_type, Product.__subclasses__())) # See if product_type is in list of Product child subclasses
        self.model = subs[0] if len(subs) > 0 else None
        if not self.model: # Raise 404 if product_type not found
            raise HttpResponse(status=404)
        return super().get(request, *args, **kwargs)
    
    def get_range_filters(self):
        model_fields = self.model._meta.fields
        field_dicts = []
        forbidden_field_names = ['rating', 'in_stock', 'sold', 'bonus_points']
        for field in model_fields:
            if isinstance(field, PositiveIntegerField) and field.name not in forbidden_field_names:
                max_value = getattr(self.model.objects.all().order_by('-'+field.name)[0], field.name)
                min_value = getattr(self.model.objects.all().order_by(field.name)[0], field.name)
                field_dict = {
                    'title': field.name.replace('_', ' '),
                    'param_name': field.name + '_gap',
                    'max': max_value,
                    'min': min_value
                }
                field_dicts.append(field_dict)
        return field_dicts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'supercategory': self.model,
            'supercategory_title': self.model.__name__,
            'filter_cats': self.model.get_type_cats(),
            'range_filters': self.get_range_filters(),
        })
        return context


class ProductView(DetailView):
    model = Product
    template_name = "store/product.html"    
    context_object_name = "product"

    def get_context_data(self, object, *args, **kwargs):
        context = super().get_context_data()
        Supercat: Product = object.__class__
        context.update({
            'supercat': {
                'name': Supercat.__name__,
                'url': Supercat.get_absolute_url_to_type() if issubclass(Supercat, Product) else '/products/',
            },
            'personal_rating': int(object.votes.filter(user=self.request.user)[0].value) if object.votes.filter(user=self.request.user) else None,
            'in_fav': self.request.user.favourite.products.contains(object) if self.request.user.is_authenticated else None,
            'in_cart': self.request.user.cart.products.contains(object) if self.request.user.is_authenticated else None,
        })
        return context


class SearchView(ListView):
    pass
    

class ProductContainerView(TemplateView, ContextMixin):
    """ Anscestor for the views ment to show products in a product container such as Cart or Favourite. """
    template_name = 'store/product_container.html'


class CartView(ProductContainerView):

    def get_context_data(self):
        return {
            'container_name' : 'cart',
            'in_container' : self.request.user.get_cart_count(),
            'products': self.request.user.cart.products.all(),
        }


class FavouriteView(ProductContainerView):

    def get_context_data(self):
        return {
            'container_name' : 'favourite',
            'in_container' : self.request.user.get_favourite_count(),
            'products': self.request.user.favourite.products.all(),
        }


# Function Based Views