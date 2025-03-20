from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from catalog.models import Product


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(10_000_000_000), MaxValueValidator(99_999_999_999)] # Формат РФ +7...
    )
    deliveryType = models.CharField(max_length=4, null=False) # free / paid
    paymentType = models.CharField(max_length=7, null=False) # online / offline
    totalCost = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=8, null=False) # accepted / rejected
    city = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)
    products = models.ManyToManyField(Product, related_name='order')
