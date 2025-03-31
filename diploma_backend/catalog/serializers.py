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


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = (
            'author',
            'email',
            'text',
            'rate',
            'date'
        )


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = (
            'name',
            'value'
        )


class ProductShortSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор товара для вкладки каталога.
    Включает все поля кроме `fullDescription`, `specifications`, служебные поля,
    а также заместо отзывов только их кол-во.
    """

    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
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


class ProductFullSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор товара для страницы подробного описания.
    Содержит все поля, кроме служебных.
    """

    tags = TagSerializer(many=True)
    images = ProductImageSerializer(many=True)
    reviews = ReviewsSerializer(many=True)
    specifications = SpecificationsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'specifications',
            'rating',
        )


class SaleProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'price',
            'title',
            'images'
        )
