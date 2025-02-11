from rest_framework import serializers
# TODO
from .models import Product, Tag, Image, Reviews, Specifications


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
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


# Возможно придется переименовать
class ProductShortSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    images = ImageSerializer(many=True)
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
