import os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


def upload_profile_avatar_to(instance: 'ProfileImage', filename: str) -> str:
    return 'profile_images/profile_{id}/{filename}'.format(
        id=instance.profile.pk, filename=filename
    )


class Profile(models.Model):
    """
    Профиль пользователя
    """

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['pk', 'user']

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_index=True)
    fullName = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(10_000_000_000), MaxValueValidator(99_999_999_999)] # Формат РФ +7...
    )
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile {self.pk}. User {self.user.pk}'


class ProfileImage(models.Model):
    """
    Аватар профиля
    """

    class Meta:
        verbose_name = 'Profile image'
        verbose_name_plural = 'Profile images'
        ordering = ['pk']

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='avatar', db_index=True)
    src = models.ImageField(null=True, blank=True, upload_to=upload_profile_avatar_to)
    alt = models.CharField(max_length=100, default='Not Found.')

    def __str__(self):
        return f'Profile image {self.pk}. Profile {self.profile.pk}'

    def save(self, *args, **kwargs):
        """
        Переопределяем метод сохранения модели.
        Добавлен функционал очистки неиспользуемых файлов.
        """

        # Получаем предыдущее изображение.
        try:
            old_obj = ProfileImage.objects.get(pk=self.pk)
            old_image = old_obj.src
        except ProfileImage.DoesNotExist:
            old_image = None

        # Сохраняем с текущим изображением
        super().save(*args, **kwargs)

        current_image = self.src

        # Будет работать только в случае появления нового файла, т.е. загрузки нового изображения.
        # Даже если будет загружен такой же файл,
        # Django не позволит им находиться в одной папке и добавит в название "соль" => старый файл удалится.
        if current_image != old_image and old_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
