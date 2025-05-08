from django.db import models
from django.contrib.auth.models import User

from catalog.models import Product


class BasketItem(models.Model):
    """
    Промежуточная модель с кол-вом товара
    """
    class Meta:
        verbose_name = 'Basket item'
        verbose_name_plural = 'Baskets items'
        unique_together = ('basket', 'product')
        ordering = ['pk']

    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.pk}. Basket {self.basket.pk}. Product {self.product.pk}'


class Basket(models.Model):
    """
    Корзина пользователя
    """
    class Meta:
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'
        ordering = ['pk']

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    basket_key = models.UUIDField(editable=False, unique=True, blank=True, null=True)
    product = models.ManyToManyField(Product, related_name='basket', through=BasketItem)

    def __str__(self):
        return f'Basket {self.pk}'
