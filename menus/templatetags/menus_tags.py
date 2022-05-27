from django import template

from ..models import Menu

register = template.Library()


# @register.simple_tag()
# def get_menu(slug):
#     return Menu.objects.get(slug=slug)

@register.simple_tag()
def get_menu(slug):
    """returning all menu objects wih the slug of 'slug' :parameter"""
    try:
        return Menu.objects.get(slug=slug)
    except:
        return None


@register.simple_tag()
def get_all_menus():
    """returning all menu objects wih the slug of 'slug' :parameter"""
    return Menu.objects.all().order_by("sequence")


