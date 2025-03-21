from django.urls import path

from .views import (
    OrdersView,
    OrderDetailView,
    PaymentView
)

app_name = 'order'

urlpatterns = [
    path('orders', OrdersView.as_view(), name='order_history'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('payment/<int:pk>', PaymentView.as_view(), name='order_payment'),
]
