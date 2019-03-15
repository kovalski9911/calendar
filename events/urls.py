from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (

    EventListView,
    EventCreateView,
    EventDeleteView,

    UserRegisterView
    )
from .apiviews import EventList


app_name = 'events'

urlpatterns = [
    # API
    path('api/list/', EventList.as_view(), name='api-event-list'),
    # path('api/create/', EventCreate.as_view(), name='api-event-create'),
    # path('api/detail/<int:pk>', EventDetail.as_view(), name='api-event-detail'),

    # base
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='events/logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(template_name='events/register.html'), name='register'),

    path('list/', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('delete/<int:pk>', EventDeleteView.as_view(), name='event-delete'),
]
