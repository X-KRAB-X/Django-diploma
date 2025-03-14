from django.db import models
from django.contrib.auth.models import User

from catalog.models import Product


class BasketItem(models.Model):
    """
    Промежуточная модель с кол-вом товара
    """
    class Meta:
        unique_together = ('basket', 'product')
        ordering = ['pk']

    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)


class Basket(models.Model):
    class Meta:
        ordering = ['pk']

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    basket_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='basket', through=BasketItem)

    def __str__(self):
        return f'Basket {self.pk}'
