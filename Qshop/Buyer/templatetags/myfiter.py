from django import template
register = template.Library()
@register.filter(name="Yf")
def yf (num):
    num = num + 10
    return num