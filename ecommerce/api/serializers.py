from rest_framework import serializers
from store.models import Product, Category, Subcategory
from account.models import Account


# Serializers
class ProductSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField(source='get_url')
    personal_rating = serializers.SerializerMethodField('personal_rating_func')
    article = serializers.SerializerMethodField('format_article')

    class Meta:
        model = Product
        fields = [
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
        ]

    def personal_rating_func(self, obj):
        try:
            return obj.get_personal_rating(user=self.context.get('request').user)
        except:
            return None

    def format_article(self, obj):
        stringified_num = str(obj.article)
        while len(stringified_num) < 18:
            stringified_num = '0' + stringified_num        
        return stringified_num

    def get_url(self, obj):
        return obj.get_absolute_url()