from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<int:item_id>/', views.index, name='index'),
]
