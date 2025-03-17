import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.views import get_basket

# Должен проверять только наличие
class AuthSignInView(APIView):
    def post(self, request: Request) -> Response:
        # Десериализуем тело запроса
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
