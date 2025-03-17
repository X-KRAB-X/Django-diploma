from django.urls import path

from .views import (
    AuthSignInView,
    AuthSignUpView,
    AuthSignOutView
)

app_name = 'auth_shop'

urlpatterns = [
    path('sign-in', AuthSignInView.as_view(), name='auth_shop_sign_in'),
    path('sign-up', AuthSignUpView.as_view(), name='auth_shop_sign_up'),
    path('sign-out', AuthSignOutView.as_view(), name='auth_shop_sign_out'),
]
