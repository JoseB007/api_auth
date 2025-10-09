from rest_framework import serializers

from .models import Post, Like

from apps.usuarios.serializers import UserReadSerializer



class PostModelSerializer(serializers.ModelSerializer):
    autor = UserReadSerializer(read_only=True)
    detalle_url = serializers.HyperlinkedIdentityField(
        view_name="post-detail",
        lookup_field="pk"
    )
    f_creacion = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True,
    )
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "detalle_url",
            "uuid",
            "titulo",
            "cuerpo",
            "likes_count",
            "autor",
            "f_creacion",
            "f_actualizacion",
        )

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeModelSerializer(serializers.ModelSerializer):
    # detalle_post = serializers.SerializerMethodField()
    post = serializers.CharField(source="post.titulo", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    f_creacion = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Like
        # fields = ("detalle_post", "post", "user", "f_creacion")
        fields = ("id", "post", "user", "f_creacion")

    # def get_detalle_post(self, obj):
    #     return PostModelSerializer(obj.post, context=self.context).data