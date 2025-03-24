from django.contrib import admin, messages

from .models import Profile, ProfileImage


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage


@admin.action(description='Mark profile undeleted')
def mark_objects_deleted(modeladmin, request, queryset):
    queryset.update(isDeleted=False)
    modeladmin.message_user(request, 'Профили успешно помечены как актуальные.', messages.SUCCESS)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ['pk']

    list_display = (
        'pk',
        'user',
        'email',
        'phone',
        'isDeleted',
    )
    list_display_links = (
        'pk',
        'user'
    )

    inlines = [
        ProfileImageInline
    ]

    actions = [
        mark_objects_deleted
    ]

    def delete_model(self, request, obj):
        """ Мягкое удаление """
        obj.isDeleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """ Мягкое удаление """
        queryset.update(isDeleted=True)


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
