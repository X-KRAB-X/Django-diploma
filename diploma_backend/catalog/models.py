import os

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
    class Meta:
        verbose_name = 'Category image'
        verbose_name_plural = 'Category images'
        ordering = ['pk']

    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='image', db_index=True)
    src = models.ImageField(null=True, blank=True, upload_to=upload_category_image_to)
    alt = models.CharField(max_length=100, default='Not Found.')

    def __str__(self):
        return f'CategoryImage {self.pk}. Category {self.category.pk}'

    def save(self, *args, **kwargs):
        """
        Переопределяем метод сохранения модели.
        Добавлен функционал очистки неиспользуемых файлов.
        """

        # Получаем предыдущее изображение.
        try:
            old_obj = CategoryImage.objects.get(pk=self.pk)
            old_image = old_obj.src
        except CategoryImage.DoesNotExist:
            old_image = None

        # Сохраняем с текущим изображением
        super().save(*args, **kwargs)

        current_image = self.src

        # Будет работать только в случае появления нового файла, т.е. загрузки нового изображения.
        # Даже если будет загружен такой же файл,
        # Django не позволит им находиться в одной папке и добавит в название "соль" => старый файл удалится.
        if current_image != old_image and old_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)


class Tag(models.Model):
    """
    Тег
    """
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['pk', 'name']

    name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return f'{self.pk}. {self.name}'


class Product(models.Model):
    """
    Товар
    """
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['pk', 'title']

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
    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'
        ordering = ['pk']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', db_index=True)
    src = models.ImageField(null=True, blank=True, upload_to=upload_product_image_to)
    alt = models.CharField(max_length=100, default='Not Found.')

    def __str__(self):
        return f'Product image {self.pk}. Product {self.product.pk}'


class Reviews(models.Model):
    """
    Отзывы
    """
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pk', 'product']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    author = models.CharField(max_length=40, db_index=True)
    email = models.EmailField(max_length=254)
    text = models.TextField(blank=True, null=False)
    rate = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], blank=False, null=False, validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Review {self.pk}. Product {self.product.pk}'


class Specifications(models.Model):
    """
    Характеристики
    """
    class Meta:
        verbose_name = 'Specification'
        verbose_name_plural = 'Specifications'
        ordering = ['pk', 'product']

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', db_index=True)
    name = models.CharField(max_length=30, db_index=True)
    value = models.TextField(blank=True, null=False)

    def __str__(self):
        return f'Specification {self.pk}. Product {self.product.pk}'


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

    def __str__(self):
        return f'Sale {self.pk}. Product {self.product.pk}'
