from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.decorators import action

from django.contrib.auth import get_user_model

from .serializers import (
    UserReadSerializer,
    RegisterSerializer,
    UserUpdateSerializer,
    AdminUserReadSerializer,
    CustomTokenObtainPairSerializer,
)

from .permissions import (
    IsSelfOrAdmin,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Un ViewSet para manejar CRUD de usuarios.
    """
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrAdminOrReadOnly]

    # def get_queryset(self):
    #     # Solo devuelve el usuario autenticado
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         return User.objects.filter(id=self.request.user.pk)
    #     return super().get_queryset()

    def get_permissions(self):
        """
        Asigna permisos diferentes según la acción.
        """
        if self.action in ["create", "list", "retrieve"]:
            # Cualquiera puede registrarse, ver el listado o ver el detalle de un usuario
            permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Solo el dueño o un admin puede editar o eliminar (put, patch, delete)
            permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        else:
            # Para todo lo demás usuario autenticado
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
        else:
            if self.request.user.is_superuser:
                return AdminUserReadSerializer
            return UserReadSerializer
        
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mi_perfil(self, request, *args, **kwargs):
        """
        Devuelve el perfil del usuario autenticado.
        """
        if self.request.user.is_superuser:
            serializer = AdminUserReadSerializer(request.user)
        else:
            serializer = UserReadSerializer(request.user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada que hereda las funciones de TokenObtainPairView
    y que usa el serializer personalizado que contiene los datos
    del usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """
    Cierra sesión en este dispositivo.
    Recibe el refresh_token y lo invalida.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "El refresh token es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except:
            return Response(
                {"detail": "Token inválido o ya caducado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Sesión cerrada correctamente."},
            status=status.HTTP_200_OK
        )
    

class LogoutAllView(APIView):
    """
    Cierra sesión en todos los dispositivos.
    Invalida todos los refresh tokens del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)

        for token in tokens:
            obj, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(
            {"detail": "Sesión cerrada en todos los dispositivos."},
            status=status.HTTP_200_OK
        )



