from django.db.transaction import atomic
from django.db.models import F

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrdersView(APIView):
    # Только для авторизованных пользователей
    permission_classes = [IsAuthenticated]

    # Страница с историей заказов
    def get(self, request: Request) -> Response:

        # Заказы с датой по убыванию
        orders = Order.objects.filter(user=request.user).order_by('-createdAt')

        serialized = OrderSerializer(orders, many=True)

        return Response(serialized.data)

    # Создание заказа

    # Используем транзакции,
    # т.к. присутствует множество операций по созданию объектов
    @atomic
    def post(self, request: Request) -> Response:

        # Получаем профиль во избежание множества запросов.
        profile = request.user.profile

        # Здесь идет проверка последнего заказа у пользователя
        # потому как если нажимать "Оформить" и возвращаться назад - будут появляться лишние объекты.

        # Если он был успешно оформлен(isCreated = True), то создаем новый.
        # Иначе - возвращаем id последнего.
        check_order = Order.objects.filter(user=request.user).only('isCreated').last()
        if check_order and not check_order.isCreated:
            return Response({'orderId': check_order.pk})

        # Создаем объект заказа для его заполнения.
        order = Order.objects.create(
            user=request.user,
            fullName=profile.fullName,
            email = profile.email,
            phone = profile.phone,
        )

        # Наполняем заказ товарами из корзины и считаем стоимость.
        total_cost = 0
        for product in request.data:
            order.orderitem_set.create(
                product_id=product['id'],
                count=product['count']
            )
            total_cost += float(product['price']) * int(product['count'])

        order.totalCost = total_cost
        order.save()

        return Response({'orderId': order.pk})


class OrderDetailView(APIView):
    def get(self, request: Request, pk) -> Response:

        # Заказ по id
        order = Order.objects.prefetch_related('product').get(pk=pk)

        serialized = OrderSerializer(order)

        return Response(serialized.data)

    def post(self, request: Request, pk) -> Response:

        # Заказ по id, здесь QuerySet, так удобнее обновлять
        order = Order.objects.filter(pk=pk)

        # Учитываем стоимость доставки
        if request.data['deliveryType'] == 'express':
            total_cost_upscale = 500
        elif request.data['deliveryType'] == 'free' and order.totalCost < 2000:
            total_cost_upscale = 200
        else:
            total_cost_upscale = 0

        # Дописываем все поля из формы
        order.update(
            fullName=request.data['fullName'],
            email=request.data['email'],
            phone=request.data['phone'],
            deliveryType=request.data['deliveryType'],
            paymentType=request.data['paymentType'],
            city=request.data['city'],
            address=request.data['address'],
            status='accepted',
            isCreated=True,

            # Прибавляем стоимость доставки
            totalCost=F('totalCost') + total_cost_upscale
        )

        return Response({'orderId': order.first().id}, status=200)


class PaymentView(APIView):
    def post(self, request: Request, pk) -> Response:
        data = request.data

        order = Order.objects.filter(pk=pk).only('paymentType', 'isPayed').first()

        # Базовая валидация
        if len(data['number']) != 16 or int(data['number']) < 0:
            return Response({'message': 'card number must be positive number with length 16.'}, status=400)

        elif not 100 <= int(data['code']) <= 999:
            return Response({'message': 'code must be positive number with length 3.'}, status=400)

        elif not 0 < int(data['month']) < 13:
            return Response({'message': 'month must be positive number between 01 and 12.'}, status=400)

        elif not 2000 <= int(data['year']) <= 2100:
            return Response({'message': 'year must be positive number between 2000 and 2100.'}, status=400)

        # Подтверждаем оплату
        order.isPayed = True
        order.save()

        return Response({}, status=200)
