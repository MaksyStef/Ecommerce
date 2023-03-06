from django import template
from api.serializers import ProductSerializer
import re
import json
register = template.Library()


@register.simple_tag
def products_to_json(queryset):
    return json.dumps(ProductSerializer(queryset, many=True).data)