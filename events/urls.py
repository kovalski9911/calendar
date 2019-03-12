from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    EventListView,
    EventCreateView,

    UserRegisterView
    )

app_name = 'events'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('register/', UserRegisterView.as_view(template_name='events/register.html'), name='register'),

    path('list/', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
]
