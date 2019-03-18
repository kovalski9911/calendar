from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Event

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'id', 'username', 'email'


class EventListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Event
        fields = 'author', 'name', 'date', 'reminder_date'


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = 'name', 'date', 'reminder'
