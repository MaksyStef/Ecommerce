from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions, status, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from store.models import Product, Flashlight, Melee, Knife, Accompanying, Souvenir, Order

import json
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.filter(sellable=True)

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'rating', 'sold']

    def get_suggestions(self):
        obj = self.get_object()
        similar_objects = obj.__class__.objects.exclude(
            pk=obj.pk
        ).filter(
            subcats__id__in=obj.subcats.all().values_list('id', flat=True)
        ).order_by(*['-created_at'], *[x.replace(' ', '_') for x in obj.get_properties()])
        return similar_objects
    
    def get_buy_altogether(self):
        obj = self.get_object()
        return obj.buy_altogether.all()

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
            if "exclude_" in param:
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
        if field_name == "rating":
            filter_kwargs = {
                f"{field_name}__in": param['exclude_list'],
            }
        return queryset.exclude(**filter_kwargs) # same to qst.filter(field__in=exclude_list)


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


    @action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny],
            url_path='suggestions', url_name='suggestions')
    def suggestions_view(self, request, *args, **kwargs):
        products = self.get_suggestions()
        serializer = self.serializer_class(products, many=True)
        return JsonResponse(data=serializer.data, safe=False)

    @action(methods=['get'], detail=True, permission_classes=[permissions.AllowAny],
            url_path='buy-altogether', url_name='buy_altogether')
    def buy_altogether_view(self, request, *args, **kwargs):
        products = self.get_buy_altogether()
        serializer = self.serializer_class(products, many=True)
        return JsonResponse(data=serializer.data, safe=False)

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


class OrderViewSet(viewsets.ViewSet):
    serializer_class = serializers.OrderSerializer

    @action(
        methods=['post', 'put', 'get'], detail=False, 
        permission_classes=[permissions.IsAuthenticated],
        authentication_classes=[SessionAuthentication],
        url_path='create-paypal-order', url_name='create_paypal_order'
    )
    def create_paypal_order(self, request):
        user = request.user
        cart = user.cart
        items = []
        for order in cart.orders.all():
            product = order.product
            items.append({
                'name': product.title,
                'description': product.description,
                'sku': str(product.id),
                'unit_amount': {
                    'currency_code': 'EUR',
                    'value': str(product.price),
                },
                'quantity': str(order.quantity),
            })

        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body({
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "EUR",
                        "value": str(cart.get_payment_price()),
                        "breakdown": {
                            "item_total": {
                                "currency_code": "EUR",
                                "value": str(cart.get_payment_price()),
                            },
                            # "discount": user.discount,
                        }
                    },
                    "items": items
                }
            ],
            "application_context": {
                "return_url": settings.PAYPAL_RETURN_URL,
                "cancel_url": settings.PAYPAL_CANCEL_URL
            }
        })

        try:
            response = settings.PAYPAL_CLIENT.execute(request)
            order_id = response.result.id
            return Response({'order_id': order_id}, status=status.HTTP_201_CREATED)

        except HttpError as e:
            error_message = json.loads(e.message)
            return Response({'error_message': error_message}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'put', 'get'], detail=False, 
        permission_classes=[permissions.IsAuthenticated], 
        authentication_classes=[SessionAuthentication],
        url_path='capture-paypal-order', url_name='capture_paypal_order'
    )
    def capture_paypal_order(self, request):
        user = request.user
        cart = user.cart
        data = request.data
        request = OrdersCaptureRequest(data['order_id'])
        request.prefer('return=representation')
        try:
            response = settings.PAYPAL_CLIENT.execute(request)
            if response.result.status == 'COMPLETED':
                cart.orders.all().update(capture_id=response.result.id)
                # user.history = user.history.all() | cart.orders.all()
                cart.orders.clear()
                return Response({'success': True})
            else:
                return Response({'error': 'Order was not completed.'}, status=status.HTTP_400_BAD_REQUEST)

        except HttpError as e:
            error_name    = json.loads(e.name)
            error_message = json.loads(e.message)
            error_details = json.loads(e.details)
            return Response({'error_name': error_name, 'error_message': error_message['message'], 'details': error_details}, status=status.HTTP_400_BAD_REQUEST)