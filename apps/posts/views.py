from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostModelSerializer
from .permissions import IsAuthorOrReadOnly


    
# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [AllowAny]


# class PostDetailView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [AllowAny]


# class PostCreateView(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(autor=self.request.user)


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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mis_posts(self, request):
        """
        Devuelve solo los posts del usuario autenticado
        """
        posts = Post.objects.filter(autor=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)