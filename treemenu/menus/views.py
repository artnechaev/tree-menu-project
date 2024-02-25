from django.shortcuts import render, get_object_or_404

from .models import MenuItem


def index(request, item_id=None):

    sel_item = None

    # дополнительный запрос к БД для получения выбранного пункта меню
    if item_id:
        sel_item = get_object_or_404(MenuItem.objects.select_related('menu'), id=item_id)
    context = {
        'title': 'Main page',
        'sel_item': sel_item,
    }

    return render(request, 'menus/index.html', context=context)
