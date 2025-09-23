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