from rest_framework import serializers

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

    def create(self, validated_data):
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
