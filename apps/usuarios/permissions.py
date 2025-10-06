from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """El dueño o el admin puede editar su perfil."""
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser


class IsAuthorOrReadOnly(permissions.BasePermission):
    """El dueño puede editar, los demás solo leer el post."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.autor == request.user
    

class IsAdminOrReadOnly(permissions.BasePermission):
    """Los superusuarios pueden editar, los demás solo leer el post."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Solo permite escribir (POST, PUT, DELETE) a los superusuarios
            return True
        return request.user.is_superuser

