from rest_framework import serializers

from .models import Basket
from catalog.models import Product

# Берем готовый сериализатор
from catalog.serializers import ProductShortSerializer


# Наследуемся от сериализатора товаров и редактируем поля
class BasketProductSerializer(ProductShortSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating',
        )
