from django.db import models

from django.contrib.auth.models import User

import uuid

# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    uuid = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False)
    titulo = models.CharField(max_length=250, verbose_name="Título")
    cuerpo = models.TextField(verbose_name="Cuerpo")
    likes = models.ManyToManyField(User, through="Like", related_name="liked_posts")
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Creación")
    f_actualizacion = models.DateField(auto_now=True, verbose_name="Actualización")

    class Meta:
        ordering = ["-f_actualizacion"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.titulo}, ({self.autor})"
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes_posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_posts")
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Creación")

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.post.titulo} - by, {self.user}"
