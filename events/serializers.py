from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Event

User = get_user_model()


class EventListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Event
        fields = '__all__'


class EventCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Event
        fields = 'author', 'name', 'date', 'reminder'
