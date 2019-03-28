from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from django.utils import timezone

from datetime import datetime

from django.contrib.auth import get_user_model
from .models import Event
from .serializers import (
    EventListSerializer,
    EventCreateSerializer,
    )


User = get_user_model()


@api_view(['POST'])
def event_list_per_day(request):
    """List of events for a per day"""
    date = request.data['date']
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        if date >= timezone.datetime.now():
            events = Event.objects.filter(
                start_date__year=date.year,
                start_date__month=date.month,
                start_date__day=date.day,
                author=request.user
            )
            data = EventListSerializer(events, many=True).data
            return Response(data)
        else:
            return Response({'error': 'Enter a correctly date'},
                            status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'not date format. Enter the date in format yyyy-mm'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def event_list_per_month(request):
    """List of events for a month"""
    date = request.data['date']
    try:
        date = datetime.strptime(date, '%Y-%m')
        today = timezone.datetime.now()
        if date.year >= today.year and date.month >= today.month:
            events = Event.objects.filter(
                start_date__year=date.year,
                start_date__month=date.month,
                author=request.user
            )
            data = EventListSerializer(events, many=True).data
            return Response(data)
        else:
            return Response({'error': 'Enter a correctly date'},
                            status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'not date format. Enter the date in format yyyy-mm-dd'},
                        status=status.HTTP_400_BAD_REQUEST)


class EventList(APIView):
    """List of events or create a new event"""

    def get(self, request, ):
        events = Event.objects.filter(author=request.user)
        data = EventListSerializer(events, many=True).data
        return Response(data)

    def post(self, request):
        event_create = EventCreateSerializer(data=request.data)
        print(request.data)
        if event_create.is_valid():
            event_create.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    """Retrieve or delete event instance"""

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
