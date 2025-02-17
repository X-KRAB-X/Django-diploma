from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Product, Tag, Category
from .serializers import (
    ProductShortSerializer,
    TagSerializer,
    CategorySerializer
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
                    freeDelivery=True if params.get('filter[freeDelivery]') == 'true' else False
                )
                .order_by(
                    # Проверка направления сортировки
                    params.get('sort') if params.get('sortType') == 'inc' else '-' + params.get('sort')
                )
                .defer('fullDescription')
            )
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
        categories = Category.objects.select_related('image')
        serialized = CategorySerializer(categories, many=True)

        return Response(serialized.data)
