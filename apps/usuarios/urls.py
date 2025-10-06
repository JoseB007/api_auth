from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.usuarios.views import (
    UserViewSet, 
    CustomTokenObtainPairView,
    LogoutView,
    LogoutAllView,
)

router = routers.DefaultRouter()
router.register(r"api/usuarios", UserViewSet, basename="usuario")

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/logout-all/', LogoutAllView.as_view(), name="logout_all"),
]