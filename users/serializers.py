from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serialize user registration"""

    password = serializers.CharField(write_only=True)
    country = serializers.CharField(required=False, allow_null=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            country=validated_data['country']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'country')


class UserSerializer(serializers.ModelSerializer):
    """Serialize user model"""

    class Meta:
        model = User
        fields = ('id', 'email')
