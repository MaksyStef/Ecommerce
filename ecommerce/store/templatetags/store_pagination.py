from django import template
from django.core.paginator import Paginator
import re

register = template.Library()


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=3, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, 
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)

@register.simple_tag
def get_number_page_link(number: int, url):
    match = re.search(pattern="page=[0-9]+", string=url)
    if match:
        url = url.replace(match.group(), f'page={number}')
    else:
        if url.find('?') != -1:
            url+= f"&page={number}"
        else:
            url+= f"?page={number}"
    return url

@register.simple_tag(takes_context=True)
def get_prev_page_link(context, url) -> str:
    """ Receives context and current url, returns absolute path to the previous page. """
    page_obj = context.get('page_obj')
    if page_obj.has_previous():
        url = get_number_page_link(page_obj.previous_page_number(), url)
    return url

@register.simple_tag(takes_context=True)
def get_next_page_link(context, url):
    """ Receives context and current url, returns absolute path to the previous page. """
    page_obj = context.get('page_obj')
    if page_obj.has_next():
        url = get_number_page_link(page_obj.next_page_number(), url)
    return url