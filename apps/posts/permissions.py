from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Solo el autor del post puede editarlo o borrarlo.
    Los demás solo pueden leer.
    """

    def has_object_permission(self, request, view, obj):
        # Lectura: siempre permitido
        if request.method in permissions.SAFE_METHODS:
            return True
        # Escritura: solo el autor
        return obj.autor == request.user
    

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Los superusuarios pueden editar, los demás solo leer el post.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser