from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from user_auth.models import User
from user_auth.serializer import UserSerializer, MyTokenObtainPairSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    """представление (view) для получения JWT-токена."""
    serializer_class = MyTokenObtainPairSerializer
