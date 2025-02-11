from django.contrib import admin

from .models import (
    Product,
    Category,
    Tag,
    Image,
    Reviews,
    Specifications
)


class ProductImages(admin.TabularInline):
    model = Image

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'price',
        'count',
        'date',
        'description_short',
        'rating',
        'freeDelivery',
    )
    list_display_links = (
        'pk',
        'title',
    )

    inlines = [
        ProductImages,
    ]

    def description_short(self, obj: Product):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        else:
            return obj.description


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
    )
    list_display_links = (
        'pk',
        'name',
    )


@admin.register(Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    list_display_links = (
        'pk',
        'name',
    )


@admin.register(Image)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'src',
        'alt'
    )
    list_display_links = (
        'pk',
    )


@admin.register(Reviews)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'author',
        'email',
        'rate',
        'date'
    )
    list_display_links = (
        'pk',
        'author',
    )


@admin.register(Specifications)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'name',
        'value'
    )
    list_display_links = (
        'pk',
        'name',
    )
