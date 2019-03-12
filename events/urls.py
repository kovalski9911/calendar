from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    EventListView,
    EventCreateView,
    )

app_name = 'events'

urlpatterns = [
    path('welcome/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),

    path('list/', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
]
