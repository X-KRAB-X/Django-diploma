from django.contrib import admin

from .models import Profile, ProfileImage


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ['pk']

    list_display = (
        'pk',
        'user',
        'email',
        'phone'
    )
    list_display_links = (
        'pk',
        'user'
    )

    inlines = [
        ProfileImageInline
    ]


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    ordering = ['pk']

    list_display = (
        'pk',
        'profile',
        'src',
        'alt'
    )
    list_display_links = (
        'pk',
        'profile'
    )
