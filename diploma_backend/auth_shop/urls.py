from django.urls import path

from .views import AuthSignInView

app_name = 'auth_shop'

urlpatterns = [
    path('sign-in', AuthSignInView.as_view(), name='auth_shop_sign_in'),
]
