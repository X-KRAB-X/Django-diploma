from django.urls import path

from .views import (
    ProfileView,
    ProfilePasswordView,
    ProfileAvatarView
)

app_name = 'profile_shop'

urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile_shop_profile'),
    path('profile/password', ProfilePasswordView.as_view(), name='profile_shop_password'),
    path('profile/avatar', ProfileAvatarView.as_view(), name='profile_shop_avatar'),
]
