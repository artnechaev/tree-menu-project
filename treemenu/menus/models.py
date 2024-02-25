from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """Модель для основных меню"""

    name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для пунктов меню"""

    name = models.CharField(max_length=150)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    path = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['menu', 'path']

    def get_path(self):
        """Получение полного пути к пункту меню"""
        if self.parent:
            path = f'{self.parent.path} > {self.name}'
        else:
            path = f'{self.name}'
        return path

    def save(self, *args, **kwargs):
        """
        Переопределение save() для сохранения полного пути к пункту меню и
        принудительного изменения меню на меню родителя
        """
        self.path = self.get_path()
        if self.parent:
            self.menu = self.parent.menu
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index', kwargs={'item_id': self.id})
