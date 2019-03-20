from django.urls import path

from .views import (

    EventListView,
    EventCreateView,
    EventDeleteView,
)
from .apiviews import (
    EventList,
    EventDetail,

    event_list_per_day,
    event_list_per_month
)


app_name = 'events'

urlpatterns = [
    # API
    path('api/list-per-day/', event_list_per_day, name='api-event-list-per-day'),
    path('api/list-per-month/', event_list_per_month, name='api-event-list-per-month'),

    path('api/list/', EventList.as_view(), name='api-event-list'),
    path('api/create/', EventList.as_view(), name='api-event-create'),
    path('api/detail/<int:pk>/', EventDetail.as_view(), name='api-event-detail'),
    path('api/delete/<int:pk>/', EventDetail.as_view(), name='api-event-delete'),

    # base
    path('list/', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
]
