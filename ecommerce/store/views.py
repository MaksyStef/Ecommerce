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
    if Knife.objects.all().count() < 64:
        for i in range(1, 65 - Knife.objects.all().count()):
            Knife.objects.create(
                price        = 100, 
                discount     = 10,
                sellable     = True,
                title        = f'Knife {i}',
                description  = f'Knife {i} description',
                article      = f'0000000{i}' if i < 10 else f'000000{i}',
                in_stock     = i,
                total_length = i*1.2,
                edge_length  = i*1.2,
                edge_width   = i*1.2,
            )
    extra_context = {
        'bestsellers' : Product.objects.all().order_by('sold')[:16],
        'brandnews_1' : Product.objects.all().order_by('created_at')[:9],
        'brandnews_2' : Product.objects.all().order_by('created_at')[9:18],
        'discounted_1': Product.objects.all().order_by('discount')[:16],
        'discounted_2': Product.objects.all().order_by('discount')[16:32],
        'discounted_3': Product.objects.all().order_by('discount')[32:48],
        'discounted_4': Product.objects.all().order_by('discount')[48:64],
    }


class NewslettersView(View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'sign':
            newsletter.sign(request.GET.get('email'))
        elif request.POST.get('action') == 'unsign':
            newsletter.unsign(request.GET.get('email'))
        return HttpResponse('success')


class ProductActionView(View):
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'toggle_fav':
            fav.toggle(
                fav=request.user.favourite,
                product=get_object_or_404(
                    Product, pk=request.POST.get('product_id'))
            )
        elif action == 'toggle_cart':
            cart.toggle(
                fav=request.user.favourite,
                product=get_object_or_404(
                    Product, pk=request.POST.get('product_id'))
            )
        elif action == 'rate':
            product = get_object_or_404(
                Product, pk=request.POST.get('product_id'))
            product.votes.create(
                user=request.user,
                value=request.POST.get('value'),
            )
        else:
            return HttpResponse('error', status=404)
        return HttpResponse('success')


class ProductsView(ListView, ContextMixin):
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 24

    extra_context = {
        'filter_cats': Category.objects.all(),
        'max_price': Product.objects.all().order_by('-price')[0].price,
        'min_price': Product.objects.all().order_by('price')[0].price,
    }
    
    def get_queryset(self):
        request = self.request

        if request.GET.get('subcategory_id'):
            queryset = Product.get_all_child_products()

        elif request.GET.get('category_id'):
            queryset = queryset.filter(cat_id=request.GET.get('category_id'))
        
        if request.GET.get('ordering'):
            queryset = queryset.order_by(request.GET.get('ordering'))
        
        if request.GET.get('count'):
            lim = int(request.GET.get('count'))
            queryset = queryset[:lim]

        if request.GET.get('price_span'):
            cheapest, expensiest = request.GET.get('price_span').split('_')
            queryset = queryset.filter(price__lte=int(cheapest), price__gte=int(expensiest))
        return queryset

    # def get(self, request, *args, **kwargs):
    #     if request.GET.get('subcategory_id'):
    #         self.extra_context.update({
    #             'prods_cat': Subcategory.objects.get(id=int(request.GET.get('subcategory_id')))
    #         })
    #     elif request.GET.get('category_id'):
    #         self.extra_context.update({
    #             'prods_cat': Category.objects.get(id=int(request.GET.get('category_id')))
    #         })
    #     return super().get(request, *args, **kwargs)


class CertainProductsView(ListView, ContextMixin):
    template_name = 'store/products.html'
    context_object_name = 'products'

    def get(self, request, product_type, *args, **kwargs):
        subs = filter(lambda cls: cls.__name__ == product_type, Product.__subclasses__())
        self.model = subs[0] if len(subs) > 0 else None
        return super().get(request, *args, **kwargs)


class ProductView(DetailView):
    template_name = "store/product.html"    


class SearchView(ListView):
    pass

# Function Based Views