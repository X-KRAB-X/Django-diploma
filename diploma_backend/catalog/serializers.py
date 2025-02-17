from rest_framework import serializers

from .models import (
    Category,
    Product,
    Tag,
    ProductImage,
    CategoryImage,
    Reviews,
    Specifications,
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'src',
            'alt'
        )


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = (
            'src',
            'alt'
        )


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'image',
            'subcategories'
        )

    # Пока что подкатегорий нет
    def get_subcategories(self, obj):
        return []


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


# Возможно придется переименовать
class ProductShortSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'count',
            'date',
            'description',
            'rating',
            'freeDelivery',
            'category',
            'images',
            'tags',
        )
