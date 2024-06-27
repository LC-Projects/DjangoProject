from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def dict_filter(value):
    # Your custom filter logic goes here
    return value


# tag for knowing the path we are in
@register.filter(name='is_path')
def is_path(request, named_url):
    """
    Check if the current path is the same as the path of the named URL
    """
    try:
        path = reverse(named_url)
        return request.path == path
    except Exception:
        return False
