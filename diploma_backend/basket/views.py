import uuid

from django.db import IntegrityError

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Basket
from .serializers import BasketProductSerializer


def _get_basket(request: Request) -> tuple[Basket, bool]:
    """
    Функция для получения корзины.

    Получает на вход объект Request
    Возвращает объект Basket привязанный к COOKIES или user,
    а также is_created, сообщающее о создании новых куки.

    Создана во избежание дублирования кода.
    """

    # Если корзина и куки только создались, сообщаем об этом функции
    is_created = False

    # Используем в качестве ключа к корзине - uuid
    basket_key = request.COOKIES.get('basket_key')

    # Корзина пользователя User.
    if request.user.is_authenticated:
        user = request.user

        # Пробуем получить корзину пользователя
        try:
            basket = (
                Basket.objects
                .prefetch_related('basketitem_set')
                .get(user=user)
            )
        except Basket.DoesNotExist:
            # Подразумевается, что это для новых пользователей, прошедших регистрацию.

            # Если есть ключ - привязываем пользователя к этой корзине.
            if basket_key:

                # Используем get_or_create на случай отсутствия корзины по ключу.
                basket, created_or_not = (
                    Basket.objects
                    .prefetch_related('basketitem_set')
                    .get_or_create(basket_key=basket_key)
                )
                basket.user = user
                basket.save()

            # Иначе - создаем новый ключ и корзину, уже с пользователем.
            # P.S. Редкий случай, в основном для избежания ошибок.
            else:
                basket_key = uuid.uuid4()
                basket = (
                    Basket.objects
                    .prefetch_related('basketitem_set')
                    .create(basket_key=basket_key, user=user)
                )
                is_created = True

    # Корзина только по ключу.
    elif basket_key:

        # Используем get_or_create на случай отсутствия корзины по ключу.
        basket, created_or_not = (
            Basket.objects
            .prefetch_related('basketitem_set')
            .get_or_create(basket_key=basket_key)
        )

    # Создание нового ключа и корзины
    else:

        # Подразумевается, что это для случаев первого входа на сайт
        # или сгоревших куки у не вошедших пользователей.
        basket_key = uuid.uuid4()
        basket = basket = (
            Basket.objects
            .prefetch_related('basketitem_set')
            .create(basket_key=basket_key)
        )
        is_created = True

    return basket, is_created


def _basket_serialize(basket) -> list:
    """
    Функция для сериализации продуктов в корзине.

    Получает на вход объект Basket
    Возвращает список словарей с полями продукта и кол-вом его в корзине.

    Создана во избежание дублирования кода.
    """

    basket_data = []

    # Проходимся по списку отсортированных товаров
    for basket_item in basket.basketitem_set.prefetch_related('product').order_by('product'):
        serialized = BasketProductSerializer(basket_item.product)

        # Добавляем в data ключ count, перед этим копируем словарь из сериализатора
        serialized_data_with_count = serialized.data
        serialized_data_with_count['count'] = basket_item.count

        basket_data.append(serialized_data_with_count)

    return basket_data


class BasketView(APIView):
    """
    Класс с необходимыми endpoint's корзины
    Реализует методы GET, POST, DELETE
    """

    def get(self, request: Request) -> Response:
        basket, is_created = _get_basket(request)

        basket_data = _basket_serialize(basket)

        response = Response(basket_data)

        # Если корзина была создана и ключа не было - устанавливаем новые куки с ключом сроком в неделю.
        if is_created:
            response.set_cookie(key='basket_key', value=basket.basket_key, max_age=60 * 60 * 24 * 7)

        return response

    def post(self, request: Request) -> Response:

        basket, is_created = _get_basket(request)
        try:
            # Базовая валидация
            # Если передано отрицательное либо дробное число - вызываем ошибку
            if request.data['count'] < 0 or not isinstance(request.data['count'], int):
                raise ValueError

            # Получаем QuerySet с одним товаром в корзине, а также его кол-во
            basket_item_queryset = basket.basketitem_set.filter(product_id=request.data['id'])

            # Проверяем что товар есть в корзине, иначе добавляем
            if not basket_item_queryset.exists():
                basket.basketitem_set.create(product_id=request.data['id'], count=0)

            count = basket_item_queryset.first().count

            # Обновляем QuerySet путем увеличения кол-ва товара
            # Проверяем, что товара в корзине не больше, чем на складе, т.е. Product.count
            # Если это так - указываем максимально допустимое кол-во
            if count + request.data['count'] >= basket_item_queryset.first().product.count:
                product_count = basket_item_queryset.first().product.count
                basket_item_queryset.update(count=product_count)
            else:
                basket_item_queryset.update(count=(count + request.data['count']))

        except ValueError as e:
            return Response({'message': 'count must be an integer and a positive'}, status=400)
        except KeyError as e:
            return Response({'message': f'Wrong params: {e}'}, status=400)
        except IntegrityError as e:
            if 'FOREIGN KEY' in e.args[0]:
                return Response({'message': f'No product with id {request.data["id"]}'}, status=400)

        basket_data = _basket_serialize(basket)

        response = Response(basket_data)

        # Если корзина была создана и ключа не было - устанавливаем новые куки с ключом сроком в неделю.
        if is_created:
            response.set_cookie(key='basket_key', value=basket.basket_key)

        return response

    def delete(self, request: Request) -> Response:

        basket, is_created = _get_basket(request)
        try:
            # Базовая валидация
            # Если передано отрицательное либо дробное число - вызываем ошибку
            if request.data['count'] < 0 or not isinstance(request.data['count'], int):
                raise ValueError

            # Получаем QuerySet с одним товаром в корзине, а также его кол-во
            basket_item_queryset = basket.basketitem_set.filter(product_id=request.data['id'])
            count = basket_item_queryset.first().count

            # Если приходит запрос с кол-вом равным текущему или более - товар удаляется из корзины
            if count <= request.data['count']:
                basket_item_queryset.delete()
            else:
                basket_item_queryset.update(count=(count - request.data['count']))

        except ValueError as e:
            return Response({'message': 'count must be an integer and a positive'}, status=400)
        except KeyError as e:
            return Response({'message': f'Wrong params: {e}'}, status=400)
        except (IntegrityError, AttributeError) as e:
            return Response({'message': 'Product not in basket'}, status=400)

        basket_data = _basket_serialize(basket)

        response = Response(basket_data)

        # Если корзина была создана и ключа не было - устанавливаем новые куки с ключом сроком в неделю.
        if is_created:
            response.set_cookie(key='basket_key', value=basket.basket_key)

        return response
