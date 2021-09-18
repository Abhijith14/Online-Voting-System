from django import template

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)