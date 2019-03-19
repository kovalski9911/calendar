from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from .models import Event
from .serializers import (
    EventListSerializer,
    EventCreateSerializer,
    UserRegisterSerializer
)


User = get_user_model()


class EventList(APIView):
    """
    List of events or create a new event
    """
    def get(self, request):
        events = Event.objects.filter(author=request.user)
        data = EventListSerializer(events, many=True).data
        return Response(data)

    def post(self, request):
        event_create = EventCreateSerializer(data=request.data)
        if event_create.is_valid():
            event_create.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    """
    Retrieve or delete event instance
    """

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event.author == request.user:
            data = EventCreateSerializer(event).data
            return Response(data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event.author == request.user:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ApiUserRegisterView(APIView):
    """
    Registration users
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        user_register = UserRegisterSerializer(data=request.data)
        if user_register.is_valid():
            user_register.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
