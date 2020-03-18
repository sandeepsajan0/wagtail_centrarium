from django import template
from ..models import Header

register = template.Library()

@register.inclusion_tag('base/include/header_logo.html', takes_context=True)
def get_header_logo(context):
    if Header.objects.first() is not None:
        logo = Header.objects.first().logo

    return {
        'logo': logo,
    }