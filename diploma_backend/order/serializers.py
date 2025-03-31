from rest_framework import serializers

from .models import Order
from catalog.models import Product

# Берем готовый сериализатор
from catalog.serializers import ProductShortSerializer


# Наследуемся от сериализатора товаров и редактируем поля
class _OrderProductSerializer(ProductShortSerializer):
    """
    Вспомогательный класс для сериализации товаров в ходе сериализации самого заказа.
    """

    # Все необходимые поля за исключением count,
    # оно будет добавлено из OrderItem
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


class OrderSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products'
        )

    def get_createdAt(self, obj):
        """
        Функция для преобразования даты в удобный формат из ISO 8601
        """

        return obj.createdAt.strftime('%Y-%m-%d %H.%M.%S')

    def get_products(self, obj):
        """
        Фукнция для сериализации каждого товара в заказе.

        Работает с объектом Order и промежуточной моделью OrderItem.
        Возвращает сериализованый товар с кол-вом его в заказе.
        """

        data = []
        for order_item in (
            # Оптимизируем запрос
            obj.orderitem_set
            .prefetch_related('product')
            .select_related('product__category')
            .prefetch_related('product__tags')
            .prefetch_related('product__images')
            .prefetch_related('product__reviews')
            .defer('product__count')
        ):
            serialized = _OrderProductSerializer(order_item.product)

            # Добавляем в data ключ count, перед этим копируем словарь из сериализатора
            serialized_data_with_count = serialized.data
            serialized_data_with_count['count'] = order_item.count

            data.append(serialized_data_with_count)

        return data
