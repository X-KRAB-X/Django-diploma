from django.urls import path

from .views import BasketView

app_name = 'basket'

urlpatterns = [
    path('basket', BasketView.as_view(), name='basket'),
]
