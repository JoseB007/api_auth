from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

# class CustomUser(AbstractUser):
#     ADMIN = "Administrador"
#     USER = "Usuario"
#     MODERADOR = "Moderador"

#     ROLES = (
#         (ADMIN, "Administrador"),
#         (USER, "Usuario"),
#         (MODERADOR, "Moderador"),
#     )

#     rol = models.CharField(max_length=20, choices=ROLES, default=USER)