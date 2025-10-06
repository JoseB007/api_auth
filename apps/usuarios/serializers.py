from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializer base para el modelo User.
    Define el modelo y campos mínimos compartidos.
    NO implementa create/update para que cada hijo
    controle su propia lógica.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserReadSerializer(BaseUserSerializer):
    """
    Para devolver la información de un usuario (detalle o lista).
    No incluye campos sensibles como 'password' o 'is_staff'.
    Hereda de BaseUserSerializer y se mantiene simple.
    """
    pass  # no necesita lógica extra, hereda todo de la base


class RegisterSerializer(BaseUserSerializer):
    """
    Para registrar un nuevo usuario.
    Sobrescribe 'create' para manejar el password con set_password.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('password',)

    def validate_email(self, value):
        """
        Verifica que el email no este en uso.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está en uso.")
        return value

    def create(self, validated_data):
        """
        Crea el usuario con el password encriptado.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(BaseUserSerializer):
    """
    Para actualizar datos del usuario.
    - No permite cambiar username.
    - El password se maneja aparte (puede hacerse un endpoint especial).
    """
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'email', 'first_name', 'last_name') 

    def update(self, instance, validated_data):
        # Evitamos cambios en username
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado que hereda funcionalidades de TokenObtainPairSerializer
    Esta se usará para agregar campos al serializer y poder devolver el token de 
    usuario y los datos del usuario.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Agregar info extra a la respuesta del login
        data.update({
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            }
        })

        return data


class PasswordChangeSerializer(serializers.Serializer):
    """
    Para cambiar la contraseña del usuario.
    Se suele usar en un endpoint dedicado (PATCH).
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual no es correcta.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class AdminUserReadSerializer(BaseUserSerializer):
    last_login = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("is_staff", "is_superuser", "last_login")