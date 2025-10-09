from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    # PostListView,
    # PostDetailView,
    # PostCreateView,
    # PostUpdateView,
    PostViewSet,
    LikeViewSet,
    api_root,
    # toggle_like,
)


router = DefaultRouter()
router.register(r'api/posts', PostViewSet, basename='post')
router.register(r'api/likes', LikeViewSet, basename='like')


urlpatterns = [
    # path('api/posts/', PostListView.as_view(), name="posts"),
    # path('api/posts/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    # path('api/posts/create/', PostCreateView.as_view(), name="post-create"),
    # path('api/posts/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path("", api_root),
    path("", include(router.urls)),
    # path('api/posts/<int:pk>/toogle-like/', toggle_like, name="toggle-like"),
]