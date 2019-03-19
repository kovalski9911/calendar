from django.contrib.auth import views as auth_views
from django.urls import path
from .views import UserRegisterView
from .apiviews import ApiUserRegisterView
from rest_framework.authtoken import views


app_name = 'users'

urlpatterns = [
    # API
    path('api/user/register', ApiUserRegisterView.as_view(), name='api-user-register'),
    path('api-token-auth/', views.obtain_auth_token),

    # base
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(template_name='users/register.html'), name='register'),
]
