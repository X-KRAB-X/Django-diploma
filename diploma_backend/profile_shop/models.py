from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


def upload_profile_avatar_to(instance: 'ProfileImage', filename: str) -> str:
    return 'profile_images/profile_{id}/{filename}'.format(
        id=instance.profile.pk, filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_index=True)
    fullName = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(10_000_000_000), MaxValueValidator(99_999_999_999)] # Формат РФ +7...
    )
    isDeleted = models.BooleanField(default=False)


class ProfileImage(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='avatar', db_index=True)
    src = models.ImageField(null=True, blank=True, upload_to=upload_profile_avatar_to)
    alt = models.CharField(max_length=100, default='Not Found.')
