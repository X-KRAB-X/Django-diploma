from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from catalog.models import Product


class OrderItem(models.Model):
    """
    Промежуточная модель с кол-вом товара
    """

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(10_000_000_000), MaxValueValidator(99_999_999_999)] # Формат РФ +7...
    )
    deliveryType = models.CharField(max_length=10, null=True, blank=True) # ordinary / express
    paymentType = models.CharField(max_length=10, null=True, blank=True) # '' / someone
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True) # accepted / rejected
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    product = models.ManyToManyField(Product, related_name='order', through=OrderItem)

    isPayed = models.BooleanField(default=False)

    # Вспомогательное поле, служит для проверки того, что заказ на стадии формирования.
    isCreated = models.BooleanField(default=False)

    isDeleted = models.BooleanField(default=False)
