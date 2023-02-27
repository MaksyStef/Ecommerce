from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
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


class ProductsView(ListView, ContextMixin):
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 24

    extra_context = {
        'filter_cats': Category.objects.all(),
        'max_price': Product.objects.all().order_by('-price')[0].price if Product.objects.all().count() > 0 else None,
        'min_price': Product.objects.all().order_by('price')[0].price if Product.objects.all().count() > 0 else None,
    }
    
    def get_queryset(self):
        request = self.request

        queryset = Product.objects.filter(sellable=True)

        if request.GET.get('subcategory_id'):
            queryset = queryset.filter(subcats__in=[get_object_or_404(Subcategory, id=int(request.GET.get('subcategory_id')))])

        elif request.GET.get('category_id'):
            queryset = queryset.filter(cats__in=[get_object_or_404(Category, id=int(request.GET.get('category_id')))])
        
        if request.GET.get('ordering'):
            queryset = queryset.order_by(request.GET.get('ordering'))
        
        if request.GET.get('price_span'):
            cheapest, expensiest = request.GET.get('price_span').split('_')
            queryset = queryset.filter(price__lte=int(cheapest), price__gte=int(expensiest))
        return queryset

    def get(self, request, *args, **kwargs):
        if request.GET.get('subcategory_id') or request.GET.get('category_id'):
            try:
                self.extra_context.update({
                    'prods_cat': Subcategory.objects.get(id=int(request.GET.get('subcategory_id')))
                })
            except Subcategory.DoesNotExist:
                pass
            try:
                self.extra_context.update({
                    'prods_cat': Category.objects.get(id=int(request.GET.get('category_id')))
                })
            except Category.DoesNotExist:
                pass
        return super().get(request, *args, **kwargs)


class CertainProductsView(ListView, ContextMixin):
    template_name = 'store/products.html'
    context_object_name = 'products'

    def get(self, request, product_type, *args, **kwargs):
        subs = filter(lambda cls: cls.__name__ == product_type, Product.__subclasses__())
        self.model = subs[0] if len(subs) > 0 else None
        if not self.model:
            raise HttpResponse(status=404)
        return super().get(request, *args, **kwargs)


class ProductView(DetailView):
    template_name = "store/product.html"    


class SearchView(ListView):
    pass

# Function Based Views