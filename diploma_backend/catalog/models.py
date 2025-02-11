from django.db import models
from django.db.models import ForeignKey


class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True)

    # Отображение правильных имен в админ-панели
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=30, db_index=True)


class Product(models.Model):
    title = models.CharField(max_length=30, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=True, null=False)
    fullDescription = models.TextField(blank=True, null=False)
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    freeDelivery = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    src = models.CharField(max_length=100)
    alt = models.CharField(max_length=100, default='Not Found.')


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=40, db_index=True)
    email = models.EmailField(max_length=254)
    text = models.TextField(blank=True, null=False)
    rate = models.IntegerField(blank=False, null=False)
    date = models.DateField(auto_now_add=True)


class Specifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=30, db_index=True)
    value = models.TextField(blank=True, null=False)
