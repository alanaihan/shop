from django import template

register = template.Library()

@register.filter
def comma_price(value):
    try:
        value = int(float(value))
        return f"{value:,}"
    except (ValueError, TypeError):
        return value