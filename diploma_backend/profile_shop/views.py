from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer
from .models import Profile, ProfileImage

class ProfileView(APIView):
    # Доступ только для авторизованных пользователей
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:

        # Ловим ошибку отсутствующего профиля и создаем его.
        # Возможно если User был создан за пределами сайта, например в админке
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        serialized = ProfileSerializer(profile)

        return Response(serialized.data)

    def post(self, request: Request) -> Response:

        # Ловим ошибку отсутствующего профиля и создаем его.
        # Возможно если User был создан за пределами сайта, например в админке
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        # Меняем данные
        profile.fullName = request.data['fullName']
        profile.email = request.data['email']
        profile.phone = request.data['phone']
        profile.save()

        serialized = ProfileSerializer(profile)

        return Response(serialized.data)


class ProfilePasswordView(APIView):
    # Доступ только для авторизованных пользователей
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:

        # Проверяем текущий пароль
        user: User = authenticate(username=request.user.username, password=request.data['currentPassword'])

        # Если пользователь был получен - меняем его пароль
        if user is not None:
            user.set_password(request.data['newPassword'])
            user.save()
        else:
            return Response({'message': 'wrong password!'}, status=400)

        return Response({}, status=200)


class ProfileAvatarView(APIView):
    # Доступ только для авторизованных пользователей
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:

        # Ловим ошибку отсутствующего профиля и создаем его.
        # Возможно если User был создан за пределами сайта, например в админке
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        if request.FILES.get('avatar'):

            # Проверяем, что у профиля есть аватар.
            # Если нет - создаем новый
            try:
                avatar = profile.avatar
                avatar.src = request.FILES['avatar']
                avatar.save()
            except ProfileImage.DoesNotExist:
                avatar = ProfileImage.objects.create(profile=profile, src=request.FILES['avatar'])

        return Response({}, status=200)
