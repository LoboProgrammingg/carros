# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        value = int(float(value))
        return '{:,}'.format(value).replace(',', '.')
    except (ValueError, TypeError):
        return value
