from django.contrib.auth import views as auth_views
from django.urls import path

from .views import UserRegisterView
from .apiviews import ApiUserRegisterView, ApiUserLoginView


app_name = 'users'

urlpatterns = [
    # API
    path('api/register/', ApiUserRegisterView.as_view(), name='api-user-register'),
    path("api/login/", ApiUserLoginView.as_view(), name="api-user-login"),

    # base
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(template_name='users/register.html'), name='register'),
]
