from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.StackedInline):
    """
    Inline класс для пунктов меню первого уровня для использования в админ-панели MenuAdmin
    """

    model = MenuItem
    fields = ('name',)
    extra = 0
    show_change_link = True
    verbose_name = '1st level menu item'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent=None)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuItemInline,)
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'menu')
    list_display_links = ('id', 'name')
    list_filter = ('menu',)
    readonly_fields = ('path',)

    def save_model(self, request, obj, form, change):
        """
        Переопределение save_model() для изменения путей и меню всех пунктов меню
        2го+ уровня при изменении родителя
        """
        super().save_model(request, obj, form, change)
        qs = MenuItem.objects.exclude(parent=None)
        for item in qs:
            item.save()
