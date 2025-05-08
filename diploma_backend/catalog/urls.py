from django.urls import path

from .views import (
    CatalogListView,
    TagListView,
    CategoriesListView,
    BannersListView,
    LimitedListView,
    PopularListView,
    SaleProductsListView,
    ProductDetailView,
    ProductDetailReviewView
)


app_name = 'catalog'

urlpatterns = [
    path('catalog', CatalogListView.as_view(), name='catalog_menu'),
    path('tags', TagListView.as_view(), name='catalog_tags'),
    path('categories', CategoriesListView.as_view(), name='catalog_categories'),
    path('banners', BannersListView.as_view(), name='catalog_banners'),
    path('sales', SaleProductsListView.as_view(), name='catalog_sales'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='catalog_product_detail'),
    path('product/<int:pk>/reviews', ProductDetailReviewView.as_view(), name='catalog_product_detail_review'),
    path('products/limited', LimitedListView.as_view(), name='catalog_limited'),
    path('products/popular', PopularListView.as_view(), name='catalog_popular')
]
