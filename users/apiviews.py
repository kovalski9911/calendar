from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token

from .serializers import UserRegisterSerializer, TokenSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class ApiUserRegisterView(APIView):
    """
    Registration users
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        user_register = UserRegisterSerializer(data=request.data)
        if user_register.is_valid():
            user_register.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ApiUserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request,):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user and user.is_verified:
            return Response({"token": user.auth_token.key})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
