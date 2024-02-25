from django import template

from menus.models import MenuItem

register = template.Library()


@register.inclusion_tag('menus/menu.html')
def draw_menu(menu_name, sel_item=None, items=None, parent=None):
    """Template tag для отрисовки меню с именем menu_name"""

    # получение queryset при первом вызове тега
    if items is None:
        items = MenuItem.objects.select_related('parent', 'menu').filter(menu__name=menu_name)

    # проверка соответствия меню выбранному пункту для отрисовки следующих уровней
    if sel_item and items is None and sel_item.menu.name != menu_name:
        sel_item = None

    context = {
        'menu': menu_name,
        'sel_item': sel_item,
        'items': items,
        'parent': parent,
    }

    return context
