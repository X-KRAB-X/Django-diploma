from django.urls import path

from .views import (
    CatalogListView,
    TagListView,
    CategoriesListView
)


app_name = 'catalog'

urlpatterns = [
    path('catalog', CatalogListView.as_view(), name='catalog_menu'),
    path('tags', TagListView.as_view(), name='catalog_tags'),
    path('categories', CategoriesListView.as_view(), name='catalog_categories')
]
