from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_date(value):
    try:
        date_obj = datetime.strptime(value, '%d-%m-%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return value