from rest_framework import serializers
from store.models import Product, Category, Subcategory, Order
from account.models import Account


# Serializers
class ProductSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    url = serializers.SerializerMethodField('get_url')
    personal_rating = serializers.SerializerMethodField('_personal_rating_func')
    article = serializers.SerializerMethodField('_format_article')
    votes_count = serializers.SerializerMethodField('_votes_count')
    size = serializers.SerializerMethodField('_get_size')
    materials = serializers.SerializerMethodField('_get_materials')
    in_cart = serializers.SerializerMethodField('_in_cart')
    in_favourite = serializers.SerializerMethodField('_in_favourite')

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'url',
            'price',
            'discount',
            'description',
            'article',
            'rating',
            'personal_rating',
            'image_general',
            'in_stock',
            'votes_count',
            'size',
            'materials',
            'in_cart',
            'in_favourite',
        ]

    def get_url(self, obj):
        return obj.get_absolute_url()

    def _format_article(self, obj):
        return obj.get_article()

    def _personal_rating_func(self, obj):
        try:
            return obj.get_personal_rating(user=self.context.get('request').user)
        except:
            return None

    def _votes_count(self, obj):
        return obj.votes.all().count()

    def _get_size(self, obj):
        return obj.get_size() if hasattr(obj, 'get_size') else ''

    def _get_materials(self, obj):
        return obj.get_materials() if hasattr(obj, 'get_materials') else ''

    def _in_cart(self, obj):
        return obj in self.context['request'].user.cart.get_products() if self.context['request'].user.is_authenticated else False

    def _in_favourite(self, obj):
        return self.context['request'].user.favourite.products.filter(pk=obj.pk).exists() if self.context['request'].user.is_authenticated else False


class OrderSerializer(serializers.Serializer):

    class Meta:
        model = Order
        fields = "__all__"