from django import template
from django.db.models import QuerySet
from store.models import Category

register = template.Library()

@register.simple_tag
def get_subcats(cat: Category) -> QuerySet:
    return cat.get_subcats()