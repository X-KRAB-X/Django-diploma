from rest_framework import serializers

from .models import Basket
from catalog.models import Product, ProductImage, Tag


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'src',
            'alt'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class BasketProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)
    reviews = serializers.SerializerMethodField()

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

    def get_reviews(self, obj):
        return obj.reviews.count()
