from django.contrib import admin

from .models import Basket, BasketItem


class ItemsInline(admin.TabularInline):
    model = BasketItem


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'basket_key',
    ]
    list_display_links = [
        'pk',
        'user',
        'basket_key',
    ]
    inlines = [
        ItemsInline
    ]
    ordering = ['pk']


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'basket',
        'product',
        'count'
    ]
    list_display_links = [
        'pk',
        'basket',
        'product',
    ]
    ordering = ['pk']
