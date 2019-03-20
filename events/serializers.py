from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Event
from users.serializers import UserSerializer

User = get_user_model()


class EventListSerializer(serializers.ModelSerializer):
    """Serialize list of event"""
    author = UserSerializer()

    class Meta:
        model = Event
        fields = ('author', 'name', 'start_date', 'stop_date', 'reminder_date')


class EventCreateSerializer(serializers.ModelSerializer):
    """Serialize create event"""
    def validate(self, data):
        now = timezone.now()
        if data['start_date'] <= now:
            raise serializers.ValidationError('Enter valid start_date')
        if data['stop_date'] != '':
            if data['start_date'] > data['stop_date']:
                raise serializers.ValidationError('Enter valid start_date and or stop_date')
        return data

    class Meta:
        model = Event
        fields = ('name', 'start_date', 'stop_date', 'reminder')
