from django import template
from django.db.models import QuerySet
from store.models import Category, ProductChildMixin

register = template.Library()

@register.simple_tag
def get_subcats(cat: Category) -> QuerySet:
    return cat.get_subcats()


@register.simple_tag
def get_absolute_url_to_type(model: ProductChildMixin) -> QuerySet:
    return model.get_absolute_url_to_type()