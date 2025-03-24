from django.contrib import admin, messages

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.action(description='Mark order undeleted')
def mark_objects_deleted(modeladmin, request, queryset):
    queryset.update(isDeleted=False)
    modeladmin.message_user(request, 'Заказы успешно помечены как актуальные.', messages.SUCCESS)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = (
        'pk',
        'createdAt',
        'fullName',
        'phone',
        'deliveryType',
        'paymentType',
        'totalCost',
        'status',
        'isPayed',
        'isCreated'
    )
    list_display_links = (
        'pk',
        'createdAt',
        'fullName',
        'phone'
    )
    inlines = [
        OrderItemInline
    ]

    actions = [
        mark_objects_deleted
    ]

    readonly_fields = ('createdAt',)

    fieldsets = (
        ('Информация о покупателе', {
            'fields': ('user', 'fullName', 'phone', 'email')
        }),
        ('Оплата', {
            'fields': ('totalCost', 'paymentType', 'isPayed')
        }),
        ('Информация о доставке', {
            'fields': ('deliveryType', 'city', 'address')
        }),
        ('Информация о заказе', {
            'fields': ('createdAt', 'status')
        }),
        ('Extra', {
            'fields': ('isCreated', 'isDeleted'),
            'classes': ('collapse',)
        })
    )


    def delete_model(self, request, obj):
        """ Мягкое удаление """
        obj.isDeleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """ Мягкое удаление """
        queryset.update(isDeleted=True)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ['pk']

    list_display = (
        'pk',
        'order',
        'product',
        'count'
    )
    list_display_links = (
        'pk',
        'order',
        'product',
    )
