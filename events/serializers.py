from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers

from .models import Event
from users.serializers import UserSerializer


User = get_user_model()


class EventListSerializer(serializers.ModelSerializer):
    """Serialize list of event"""

    author = UserSerializer()
    stop_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ('author', 'name', 'start_date', 'stop_date', 'reminder_date')


class EventCreateSerializer(serializers.ModelSerializer):
    """Serialize create event"""

    def validate(self, data):
        now = timezone.now()
        if data['start_date'] <= now:
            raise serializers.ValidationError('Enter valid start_date')
        if data['stop_date']:
            if data['start_date'] > data['stop_date']:
                raise serializers.ValidationError('stop date must be later than start date')
        return data

    class Meta:
        model = Event
        fields = ('name', 'start_date', 'stop_date', 'reminder')
