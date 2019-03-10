from django.contrib import admin
from django.urls import path, include
from .views import (
    ReminderListView,
    ReminderDetailView,
    ReminderCreateView,
    ReminderUpdateView,
    ReminderDeleteView,

    EventListView,
    EventCreateView,
    )

app_name = 'events'

urlpatterns = [
    path('reminder-list/', ReminderListView.as_view(), name='reminder-list'),
    path('reminder-detail/<int:pk>', ReminderDetailView.as_view(), name='reminder-detail'),
    path('reminder-create/', ReminderCreateView.as_view(), name='reminder-create'),
    path('reminder-update/<int:pk>', ReminderUpdateView.as_view(), name='reminder-update'),
    path('reminder-delete/<int:pk>', ReminderDeleteView.as_view(), name='reminder-delete'),

    path('event-list/', EventListView.as_view(), name='event-list'),
    path('event-create/', EventCreateView.as_view(), name='event-create'),
]
