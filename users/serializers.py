from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serialize user registration
    """

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            # username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize user model
    """

    class Meta:
        model = User
        fields = ('id', 'email')


class TokenSerializer(serializers.ModelSerializer):
    """
    Serialize user model
    """

    class Meta:
        model = Token
        fields = ('key',)