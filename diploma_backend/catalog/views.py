from django.core.serializers import serialize
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Product, Tag
from .serializers import ProductShortSerializer, TagSerializer


class CatalogPagination(PageNumberPagination):
    """
    Наследник `PageNumberPagination`
    Переопределяет метод `get_paginated_response`
    для получения валидного JSON
    """
    def get_paginated_response(self, data):
        return Response({
            'currentPage': self.page.number,
            # 'lastPage': dir(self.page.paginator),
            # Обязательно протестировать!!
            'lastPage': self.page.paginator.num_pages,
            'items': data
        })


class CatalogListView(APIView):
    def get(self, request: Request) -> Response:
        products = (
            Product.objects
            .prefetch_related('tags')
            .select_related('category')
        )

        paginator = CatalogPagination()
        page = paginator.paginate_queryset(products, request, view=self)
        serialized = ProductShortSerializer(page, many=True)
        return paginator.get_paginated_response(serialized.data)


class TagListView(APIView):
    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()

        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data)
