from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token

from .serializers import UserRegisterSerializer, TokenSerializer
from django.contrib.auth import get_user_model


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
            user_id = user_register['id'].value
            int(user_id)
            token = Token.objects.get(user_id=user_id)
            ts = TokenSerializer(token).data
            print(ts)
            return Response(ts)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
