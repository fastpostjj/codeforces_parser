from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user_auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'chat_id',
            'is_active',
            'is_subscripted'
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Сериализатор  MyTokenObtainPairSerializer
    для обработки запросов на получение токена
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['chat_id'] = user.chat_id
        token['email'] = user.email
        return token
