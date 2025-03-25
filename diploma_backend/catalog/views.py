from django.db.models import Sum

from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Product, Tag, Category, SaleProducts
from .serializers import (
    ProductShortSerializer,
    ProductFullSerializer,
    TagSerializer,
    CategorySerializer,
    SaleProductSerializer,
    ReviewsSerializer
)


class CatalogPagination(PageNumberPagination):
    """
    Наследник `PageNumberPagination`
    Переопределяет метод `get_paginated_response`
    для получения валидного JSON
    """

    page_size = 4
    page_query_param = 'currentPage'
    def get_paginated_response(self, data):
        return Response({
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages,
            'items': data
        })


class CatalogListView(APIView):
    def get(self, request: Request) -> Response:
        params = request.query_params
        paginator = CatalogPagination()

        # Основной вариант
        if params and params.get('format') is None:
            # Кол-во объектов(товаров) на 1 странице
            paginator.page_size = params.get('limit')

            products = (
                Product.objects
                .select_related('category')
                .prefetch_related('tags')
                .prefetch_related('images')
                .prefetch_related('reviews')
                .filter(
                    title__icontains=params.get('filter[name]'),
                    price__range=(params.get('filter[minPrice]'), params.get('filter[maxPrice]')),
                    isDeleted=False
                )
                .order_by(
                    # Проверка направления сортировки
                    params.get('sort') if params.get('sortType') == 'inc' else '-' + params.get('sort')
                )
                .defer('fullDescription', 'sortIndex', 'limited')
            )
            # Отдельная проверка бесплатной доставки
            # Если передано false - будут выведены товары с бесплатной и платной.
            if params.get('filter[freeDelivery]') == 'true':
                products = products.filter(freeDelivery=True)

            # Отдельная проверка на наличие
            if params.get('filter[available]') == 'true':
                products = products.filter(count__gt=0)

            # Фильтрация по тегам. Товар должен включать хотя бы один из переданных.
            # Без передачи тегов выводятся все товары
            if params.getlist('tags[]', default=None):
                products = products.filter(tags__in=params.getlist('tags[]')).distinct()

            # Соответствие товара выбранной категории
            if params.get('category'):
                products = products.filter(category=params.get('category'))

        # Тестовый вариант для запроса в браузере без фильтров
        else:
            products = (
                Product.objects
                .select_related('category')
                .prefetch_related('tags')
                .prefetch_related('reviews')
                .prefetch_related('images')
            )

        page = paginator.paginate_queryset(products, request, view=self)
        serialized = ProductShortSerializer(page, many=True)
        return paginator.get_paginated_response(serialized.data)


class TagListView(APIView):
    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()

        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data)


class CategoriesListView(APIView):
    def get(self, request: Request) -> Response:
        categories = Category.objects.select_related('image').filter(isDeleted=False)
        serialized = CategorySerializer(categories, many=True)

        return Response(serialized.data)


class BannersListView(APIView):
    def get(self, request: Request) -> Response:
        data = []

        # Берем по одному товару из первых трех категорий в базе.
        for category in Category.objects.prefetch_related('product_set').filter(isDeleted=False)[:3]:
            serialized = ProductShortSerializer(category.product_set.first())
            data.append(serialized.data)

        return Response(data)


class PopularListView(APIView):
    def get(self, request: Request) -> Response:
        products = (
            Product.objects
            .select_related('category')
            .prefetch_related('tags')
            .prefetch_related('images')
            .prefetch_related('reviews')
            .order_by('sortIndex', '-sold')
            .defer('fullDescription', 'sortIndex')
            .filter(isDeleted=False)
            [:8]
        )

        serialized = ProductShortSerializer(products, many=True)

        return Response(serialized.data)


class LimitedListView(APIView):
    def get(self, request: Request) -> Response:

        # Первые 16 товаров с параметром limited=True
        products = (
            Product.objects
            .select_related('category')
            .prefetch_related('tags')
            .prefetch_related('images')
            .prefetch_related('reviews')
            .filter(limited=True, isDeleted=False)
            .defer('fullDescription', 'sortIndex')
            [:16]
        )

        serialized = ProductShortSerializer(products, many=True)

        return Response(serialized.data)


class SaleProductsListView(APIView):
    def get(self, request: Request) -> Response:
        paginator = CatalogPagination()
        data = []

        sales = SaleProducts.objects.select_related('product').filter(product__isDeleted=False)
        page = paginator.paginate_queryset(sales, request, view=self)

        for discount in page:

            # Сериализуем сам товар.
            serialized = SaleProductSerializer(discount.product)
            current_discount = serialized.data

            # Дополняем получившийся словарь, указывая параметры скидки.
            current_discount['salePrice'] = discount.salePrice

            # Форматируем дату для получения валидного значения
            current_discount['dateFrom'] = discount.dateFrom.strftime('%m-%d')
            current_discount['dateTo'] = discount.dateTo.strftime('%m-%d')

            data.append(current_discount)

        return paginator.get_paginated_response(data)


class ProductDetailView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        try:
            product = Product.objects.filter(isDeleted=False).get(pk=pk)
        except Product.DoesNotExist as e:
            return Response({'message': f'Product with id: {pk} - not exists or deleted.'})

        serialized = ProductFullSerializer(product)

        return Response(serialized.data)


class ProductDetailReviewView(APIView):
    # Только для авторизованных пользователей
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk: int) -> Response:
        try:
            product = (
                Product.objects
                .prefetch_related('reviews')
                .filter(isDeleted=False)
                .only('rating')
                .get(pk=pk)
            )
        except Product.DoesNotExist as e:
            return Response({'message': f'Product with id: {pk} - not exists or deleted.'})

        product.reviews.create(
            author=request.data['author'],
            email=request.data['email'],
            text=request.data['text'],
            rate=request.data['rate']
        )

        # Изменение рейтинга товара.
        # Получаем кол-во оценок и их сумму.
        rate_count = product.reviews.count()
        rate_summ = product.reviews.aggregate(rate_summ=Sum('rate'))['rate_summ']

        # Присваиваем товару среднее арифметическое, что и является оценкой.
        product.rating = round(rate_summ / rate_count, 1)
        product.save()

        serialized = ReviewsSerializer(product.reviews, many=True)

        return Response(serialized.data)
