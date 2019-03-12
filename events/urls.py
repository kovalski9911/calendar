from django.contrib import admin
from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    )

app_name = 'events'

urlpatterns = [
    path('event-list/', EventListView.as_view(), name='event-list'),
    path('event-create/', EventCreateView.as_view(), name='event-create'),
]
