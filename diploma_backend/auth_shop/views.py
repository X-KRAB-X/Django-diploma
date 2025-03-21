import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import QueryDict

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from profile_shop.models import Profile


# Должен проверять только наличие пользователя в системе
class AuthSignInView(APIView):
    def post(self, request: Request) -> Response:

        # Десериализуем тело запроса
        if not isinstance(request.data, QueryDict):
            data = request.data
            print(data)
        else:
            data = json.loads(
                list(request.data.keys())[0]
            )

        # Базовая валидация
        if not data['username'] or not data['password']:
            return Response({'message': 'username and password required'}, status=500)

        elif len(data['username']) > 150 or len(data['password']) > 128:
            return Response({'message': 'username and password max length is 150 and 128'}, status=500)

        # Вход
        user: User = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
        else:
            return Response({'message': 'invalid credentials'}, status=500)

        return Response({}, status=200)


class AuthSignUpView(APIView):
    def post(self, request: Request) -> Response:
        # Десериализуем тело запроса
        data = json.loads(
            list(request.data.keys())[0]
        )

        # Базовая валидация
        if not data['username'] or not data['password'] or not data['name']:
            return Response({'message': 'username, password and name required'}, status=500)

        elif len(data['username']) > 150 or len(data['password']) > 128 or len(data['name']) > 150:
            return Response({'message': 'username and name max length is 150. password - 128'}, status=500)

        # Регистрация

        # Создаем в базе новый объект пользователя
        User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['name']
        )

        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:

            # Создаем профиль
            Profile.objects.create(user=user)

            login(request, user)

        return Response({}, status=200)


class AuthSignOutView(APIView):
    def post(self, request: Request) -> Response:

        # Выход
        logout(request)

        return Response({}, status=200)
