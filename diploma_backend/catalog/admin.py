from django.contrib import admin, messages

from .models import (
    Product,
    Category,
    Tag,
    ProductImage,
    CategoryImage,
    Reviews,
    Specifications,
    SaleProducts
)


class ProductImagesInline(admin.TabularInline):
    model = ProductImage


class ProductReviewsInline(admin.StackedInline):
    model = Reviews


class CategoryImagesInline(admin.TabularInline):
    model = CategoryImage


class SaleProductInline(admin.StackedInline):
    model = SaleProducts


class SpecificationsInline(admin.StackedInline):
    model = Specifications


@admin.action(description='Mark product undeleted')
def mark_objects_deleted(modeladmin, request, queryset):
    queryset.update(isDeleted=False)
    modeladmin.message_user(request, 'Товары успешно помечены как актуальные.', messages.SUCCESS)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ['pk']

    list_display = (
        'pk',
        'title',
        'price',
        'count',
        'date',
        'description_short',
        'rating',
        'freeDelivery',
        'limited',
        'isDeleted'
    )
    list_display_links = (
        'pk',
        'title',
        'description_short',
    )

    inlines = [
        SpecificationsInline,
        ProductImagesInline,
        SaleProductInline,
        ProductReviewsInline
    ]

    actions = [
        mark_objects_deleted
    ]

    readonly_fields = ('date', )

    fieldsets = (
        ('Общая информация', {
            'fields': ('title', 'description', 'fullDescription', 'price', 'freeDelivery', 'date')
        }),
        ('Продажи и наличие', {
            'fields': ('count', 'limited', 'sold', 'rating'),
            'description': 'Информация о наличии товара, кол-ве продаж и рейтинге.'
        }),
        ('Категория и теги', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',),
            'description': 'Можно изменить принадлежность товара к категории и накинуть новые теги.'
        }),
        ('Extra', {
            'fields': ('sortIndex',),
            'classes': ('collapse',)
        })
    )

    def description_short(self, obj: Product):
        if len(obj.description) > 30:
            return obj.description[:30] + '...'
        else:
            return obj.description

    def delete_model(self, request, obj):
        """ Мягкое удаление """
        obj.isDeleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """ Мягкое удаление """
        queryset.update(isDeleted=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'isDeleted',
    )
    list_display_links = (
        'pk',
        'title',
    )

    inlines = [
        CategoryImagesInline
    ]


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'category',
        'src',
        'alt'
    )
    list_display_links = (
        'pk',
        'category'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    list_display_links = (
        'pk',
        'name',
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'src',
        'alt'
    )
    list_display_links = (
        'pk',
        'product'
    )


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
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
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'name',
        'value'
    )
    list_display_links = (
        'pk',
        'product',
        'name'
    )


@admin.register(SaleProducts)
class SaleProductAdmin(admin.ModelAdmin):
    ordering = ['pk']

    list_display = (
        'pk',
        'product',
        'salePrice',
        'dateFrom',
        'dateTo'
    )
    list_display_links = (
        'pk',
        'product'
    )
