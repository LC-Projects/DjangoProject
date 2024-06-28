from django import template
from django.urls import reverse
from urllib.parse import unquote

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
    
    
    
@register.filter(name='remove_media_prefix')
def remove_media_prefix(value):
    # Decode the URL
    decoded_url = unquote(value)
    # Check if 'https://' is in the decoded URL and '/media/' is the prefix
    if decoded_url.startswith('/media/https'):
        # Remove '/media/' prefix
        return decoded_url.replace('/media/', '', 1)
    return value
