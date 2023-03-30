from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from store.models import Product, Flashlight, Melee, Knife, Accompanying, Souvenir

import json


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.filter(sellable=True)

    def get_gap_params(self) -> list[dict[str, ...]]:
        params = []
        for param, value in self.request.GET.items():
            if "_gap" in param:
                mn, mx = value.split("_")
                params.append({
                    'field_name':param,
                    'mn': int(mn), # minimum of gap
                    'mx': int(mx), # maximum of gap
                })
        return params

    def gap_filter(self, param, queryset):
        field_name = param['field_name'].replace("_gap", "")
        filter_kwargs = {
            f"{field_name}__lte": param['mx'], 
            f"{field_name}__gte": param['mn'],
        }
        return queryset.filter(**filter_kwargs) # same to qst.filter(field__lte=mx, field__gte=mn)

    def get_exclude_params(self) -> list[dict[str, ...]]:
        params = []
        for param, value in self.request.GET.items():
            if "_gap" in param:
                exclude_list = value.split(",")
                exclude_list = list(map(lambda x: int(x), exclude_list))
                params.append({
                    'field_name':param,
                    'exclude_list': exclude_list,
                })
        return params

    def exclude_filter(self, param, queryset):
        field_name = param['field_name'].replace("exclude_", "")
        filter_kwargs = {
            f"{field_name}_pk__in": param['exclude_list'],
        }
        if filter_name == "rating":
            filter_kwargs = {
                f"{field_name}__in": param['exclude_list'],
            }
        return queryset.filter(**filter_kwargs) # same to qst.filter(field__in=exclude_list)


    def get_queryset(self):
        queryset = self.queryset
        get_params = self.request.query_params.get

        if get_params('discount'):
            try:
                mn, mx = get_params('discount').split('_') # split minimal and maximal discount from 1_5 (1 to 5) format
                queryset = queryset.filter(discount__gte=int(mn), discount__lte=int(mx))
            except ValueError:
                if get_params('discount') == 'only':
                    queryset = queryset.filter(discount__gte=1)
        if get_params('in_stock')=='true':
            queryset = queryset.filter(in_stock__gte=1)
        elif get_params('in_stock')=='false':
            queryset = queryset.filter(in_stock=0)
        for param in self.get_gap_params():
            queryset = self.gap_filter(param, queryset)
        for param in self.get_exclude_params():
            queryset = self.exclude_filter(param, queryset)
        return queryset


    @action(methods=['get'], detail=False, url_path='total-count', url_name='total_count')
    def objects_total_count(self, request, *args, **kwargs):
        return JsonResponse({'total_count': self.queryset.all().count()})

    @action(methods=['put'], detail=True, permission_classes=[permissions.IsAuthenticated],
            url_path='rate', url_name='rate')
    def rate_product(self, request, *args, **kwargs):
        product = self.get_object()
        val = json.loads(request.body).get('value')
        product.rate(int(val), request.user)
        return Response()

    @action(methods=['post', 'put', 'delete'], detail=True, permission_classes=[permissions.IsAuthenticated],
            url_path='toggle-favourite', url_name='toggle_favourite')
    def toggle_favourite(self, request, *args, **kwargs):
        product = self.get_object()
        result, product = request.user.favourite.toggle(product)
        return Response()

    @action(methods=['post', 'put', 'delete'], detail=True, permission_classes=[permissions.IsAuthenticated],
            url_path='toggle-cart', url_name='toggle_cart')
    def toggle_cart(self, request, *args, **kwargs):
        product = self.get_object()
        result, product = request.user.cart.toggle(product)
        return Response()


class KnifeProductView(ProductViewSet):
    queryset = Knife.objects.filter(sellable=True)


class MeleeProductView(ProductViewSet):
    queryset = Melee.objects.filter(sellable=True)


class SouvenirProductView(ProductViewSet):
    queryset = Souvenir.objects.filter(sellable=True)


class FlashlightProductView(ProductViewSet):
    queryset = Flashlight.objects.filter(sellable=True)


class AccompanyingProductView(ProductViewSet):
    queryset = Accompanying.objects.filter(sellable=True)