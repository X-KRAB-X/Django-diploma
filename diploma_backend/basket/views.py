from itertools import product

from django.db import IntegrityError

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Basket
from .serializers import BasketProductSerializer


def get_basket(request) -> Basket:
    """
    Функция для получения корзины.

    Получает на вход объект Request
    Возвращает объект Basket привязанный к сессии или к объекту User.

    Создана во избежание дублирования кода.
    """

    if request.session.session_key is None:
        request.session.save()

    # Корзина по сессии
    if not request.user.is_authenticated:
        # Используем в качестве ключа к корзине - ключ сессии, он создается автоматически, подробнее далее.
        basket_key = request.session.get('basket_key')

        # Если ключ найден - получаем либо создаем корзину.
        # Иначе - создаем корзину и сохраняем ключ.
        if basket_key:
            try:
                basket = Basket.objects.get(basket_key=basket_key)
            except Basket.DoesNotExist:

                # Получаем ключ, создаем по нему запись в базе и сохраняем его внутри сессии
                basket_key = request.session.session_key
                basket = Basket.objects.create(basket_key=basket_key)
                request.session['basket_key'] = basket_key

        # Подразумевается, что это для случаев первого входа на сайт или же возникновения новой сессии.
        else:
            basket_key = request.session.session_key
            basket = Basket.objects.create(basket_key=basket_key)
            request.session['basket_key'] = basket_key

    # Корзина пользователя
    elif request.user.is_authenticated:
        user = request.user
        try:
            basket = Basket.objects.get(user=user)
        except Basket.DoesNotExist:
            basket = Basket.objects.create(user=user)

    return basket


def basket_serialize(basket) -> list:
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


# TODO Перенос данных делать в API логина!! Не так и плохо, что корзина очищается

# TODO Возможно, при создании заказа придется проверять еще раз сколько товаров указано
# TODO ибо пользователь может написать это вручную, но запросов на это не приходит


class BasketView(APIView):
    def get(self, request: Request) -> Response:
        basket = get_basket(request)

        basket_data = basket_serialize(basket)

        return Response(basket_data)

    def post(self, request: Request) -> Response:
        print(request.data)

        basket = get_basket(request)
        try:
            # Получаем QuerySet с одним товаром в корзине, а также его кол-во
            basket_item_queryset = basket.basketitem_set.filter(product_id=request.data['id'])

            # Проверяем что товар есть в корзине, иначе добавляем
            if basket_item_queryset.exists():
                count = basket_item_queryset.first().count

                # Если передано отрицательное либо дробное число - вызываем ошибку
                if request.data['count'] < 0 or not isinstance(request.data['count'], int):
                    raise ValueError

                # Обновляем QuerySet путем увеличения кол-ва товара
                # Проверяем, что товара в корзине не больше, чем на складе, т.е. Product.count
                elif count + request.data['count'] >= basket_item_queryset.first().product.count:
                    product_count = basket_item_queryset.first().product.count
                    basket_item_queryset.update(count=product_count)
                else:
                    basket_item_queryset.update(count=(count + request.data['count']))
            else:
                basket.basketitem_set.create(product_id=request.data['id'])

        except ValueError as e:
            return Response({'message': 'count must be an integer and a positive'}, status=400)
        except KeyError as e:
            return Response({'message': f'Wrong params: {e}'}, status=400)
        except IntegrityError as e:
            if 'FOREIGN KEY' in e.args[0]:
                return Response({'message': f'No product with id {request.data["id"]}'}, status=400)

        basket_data = basket_serialize(basket)

        return Response(basket_data)

    def delete(self, request: Request) -> Response:
        print(request.data)

        basket = get_basket(request)
        try:
            # Получаем QuerySet с одним товаром в корзине, а также его кол-во
            basket_item_queryset = basket.basketitem_set.filter(product_id=request.data['id'])
            count = basket_item_queryset.first().count

            # Если передано отрицательное либо дробное число - вызываем ошибку
            if request.data['count'] < 0 or not isinstance(request.data['count'], int):
                raise ValueError

            # Если приходит запрос с кол-вом равным текущему или более - товар удаляется из корзины
            elif count <= request.data['count']:
                basket_item_queryset.delete()
            else:
                basket_item_queryset.update(count=(count - request.data['count']))

        except ValueError as e:
            return Response({'message': 'count must be an integer and a positive'}, status=400)
        except KeyError as e:
            return Response({'message': f'Wrong params: {e}'}, status=400)
        except (IntegrityError, AttributeError) as e:
            return Response({'message': 'Product not in basket'}, status=400)

        basket_data = basket_serialize(basket)

        return Response(basket_data)
