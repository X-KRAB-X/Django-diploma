from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


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
