from rest_framework import serializers

from .models import Profile, ProfileImage


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = (
            'src',
            'alt'
        )


class ProfileSerializer(serializers.ModelSerializer):
    avatar = ProfileAvatarSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'fullName',
            'email',
            'phone',
            'avatar'
        )