from django.shortcuts import render
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

    def get_queryset(self):
        queryset = self.queryset
        get_params = self.request.query_params.get

        if get_params('limit') and queryset.count() >= int(get_params('limit')):
            queryset = queryset[:get_params('limit')]
        return queryset


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