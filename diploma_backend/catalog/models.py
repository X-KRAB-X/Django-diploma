from operator import truediv

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def upload_product_image_to(instance: 'ProductImage', filename: str):
    return 'product_images/product_{pk}/{filename}'.format(
        pk=instance.product.pk, filename=filename
    )


def upload_category_image_to(instance: 'CategoryImage', filename: str):
    return 'category_images/category_{pk}/{filename}'.format(
        pk=instance.category.pk, filename=filename
    )


class Category(models.Model):
    """
    Категория
    """
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = [
            'pk',
            'title'
        ]

    title = models.CharField(max_length=30, db_index=True)
    isDeleted = models.BooleanField(default=False)

    def delete_model(self, request, obj):
        """ Мягкое удаление """
        obj.isDeleted = True
        obj.save()

    def delete_queryset(self, request, queryset):
        """ Мягкое удаление """
        queryset.update(isDeleted=True)

    def __str__(self):
        return f'{self.pk}. {self.title}'


class CategoryImage(models.Model):
    """
    Изображение категории
    """
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='image', db_index=True)
    src = models.ImageField(null=True, blank=True, upload_to=upload_category_image_to)
    alt = models.CharField(max_length=100, default='Not Found.')


class Tag(models.Model):
    """
    Тег
    """
    class Meta:
        ordering = [
            'pk',
            'name'
        ]

    name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return f'{self.pk}. {self.name}'


class Product(models.Model):
    """
    Товар
    """
    class Meta:
        ordering = [
            'pk',
            'title'
        ]

    title = models.CharField(max_length=50, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=True, null=False)
    fullDescription = models.TextField(blank=True, null=False)
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    freeDelivery = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')

    sortIndex = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    limited = models.BooleanField(default=False)

    sold = models.PositiveIntegerField(default=0)

    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}. {self.title}: ${self.price}'


class ProductImage(models.Model):
    """
    Изображение товара
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', db_index=True)
    src = models.ImageField(null=True, blank=True, upload_to=upload_product_image_to)
    alt = models.CharField(max_length=100, default='Not Found.')


class Reviews(models.Model):
    """
    Отзывы
    """
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = [
            'pk',
            'product'
        ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    author = models.CharField(max_length=40, db_index=True)
    email = models.EmailField(max_length=254)
    text = models.TextField(blank=True, null=False)
    rate = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], blank=False, null=False, validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateField(auto_now_add=True)


class Specifications(models.Model):
    """
    Характеристики
    """
    class Meta:
        verbose_name = 'Specification'
        verbose_name_plural = 'Specifications'
        ordering = [
            'pk',
            'product'
        ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', db_index=True)
    name = models.CharField(max_length=30, db_index=True)
    value = models.TextField(blank=True, null=False)


class SaleProducts(models.Model):
    """
    Скидки на товары
    """
    class Meta:
        verbose_name = 'Sale Product'
        verbose_name_plural = 'Sale Products'
        ordering = ['pk', 'product']

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sales', db_index=True)
    salePrice = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    dateFrom = models.DateField(auto_now_add=True)
    dateTo = models.DateField(blank=False, null=False)
