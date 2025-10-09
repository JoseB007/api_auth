from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Post, Like
from .serializers import PostModelSerializer, LikeModelSerializer
from .permissions import IsSelfOrAdminOrReadOnly



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'usuarios': reverse('usuario-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'likes': reverse('like-list', request=request, format=format),
    })


# class PostUpdateView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_update(self, serializer):
#         post = self.get_object()
#         if post.autor != self.request.user:
#             raise PermissionDenied("No tienes permiso para editar este post")
#         serializer.save()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrAdminOrReadOnly]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mis_posts(self, request):
        """
        Devuelve solo los posts del usuario autenticado
        """
        posts = Post.objects.filter(autor=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return Response({
            "liked": liked,
            "likes_count": post.likes.count()
        })

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet que solo permite leer los likes (GET)"""
    queryset = Like.objects.all()
    serializer_class = LikeModelSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mis_likes(self, request):
        """
        Devuelve solo los likes del usuario autenticado
        """
        likes = Like.objects.filter(user=request.user)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)


# from rest_framework_simplejwt.authentication import JWTAuthentication

# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def toggle_like(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response({"detail": "Post no encontrado."}, status=404)

#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return Response({"likes": post.likes.count()})