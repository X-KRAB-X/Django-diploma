from django.urls import path

from .views import CatalogListView, TagListView


app_name = 'catalog'

urlpatterns = [
    path('catalog', CatalogListView.as_view(), name='catalog_menu'),
    path('tags', TagListView.as_view(), name='tags'),
]
