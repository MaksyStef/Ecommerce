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
            'filter_cats': Category.objects.all(),
            'max_price': int(self.model.objects.all().order_by('-price')[0].price)+1 if self.model.objects.all().count() > 0 else None,
            'min_price': int(self.model.objects.all().order_by('price')[0].price)    if self.model.objects.all().count() > 0 else None,
            'api_url': f'/api/{self.model.__name__.lower()}/', # Set API url depending on self.model
        })
        return context
    

class CertainProductsView(ProductsView):

    def get(self, request, product_type, *args, **kwargs):
        subs = list(filter(lambda cls: slugify(cls.__name__) == product_type, Product.__subclasses__())) # See if product_type is in list of Product child subclasses
        self.model = subs[0] if len(subs) > 0 else None
        if not self.model: # Raise 404 if product_type not found
            raise HttpResponse(status=404)
        return super().get(request, *args, **kwargs)


class ProductView(DetailView):
    model = Product
    template_name = "store/product.html"    


class SearchView(ListView):
    pass
    

class ProductContainerView(TemplateView, ContextMixin):
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