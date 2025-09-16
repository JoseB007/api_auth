from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model

from .serializers import (
    UserReadSerializer,
    RegisterSerializer,
    UserUpdateSerializer,
    CustomTokenObtainPairSerializer,
)


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada que hereda las funciones de TokenObtainPairView
    y que usa el serializer personalizado que contiene los datos
    del usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer




class UserViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet para manejar CRUD de usuarios.
    """

    queryset = User.objects.all()

    def get_queryset(self):
        # Solo devuelve el usuario autenticado
        if self.action in ['update', 'partial_update', 'destroy']:
            return User.objects.filter(id=self.request.user.pk)
        return super().get_queryset()

    def get_permissions(self):
        """
        Asigna permisos diferentes según la acción.
        """
        if self.action == "create":
            # Cualquiera puede registrarse
            permission_classes = [AllowAny]
        else:
            # Para todo lo demás, usuario autenticado
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Usa un serializer distinto según la acción.
        """
        if self.action == "create":
            return RegisterSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserReadSerializer
