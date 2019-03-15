from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Event
from .serializers import EventListSerializer, EventCreateSerializer


# def events_list(request):
#     events = Event.objects.all()
#     data = {'results': list(events.values('author', 'name', 'date', 'reminder_date'))}
#     return JsonResponse(data)


class EventList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = Event.objects.all()
        data = EventListSerializer(events, many=True).data
        return Response(data)


# class EventDetail(APIView):
#
#     def get(self, request, pk):
#         event = get_object_or_404(Event, pk=pk)
#         data = EventCreateSerializer(event).data
#         return Response(data)
#
#
# class EventCreate(generics.CreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# class EventList(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventListSerializer
#
#
# class EventDetail(generics.RetrieveDestroyAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventListSerializer
