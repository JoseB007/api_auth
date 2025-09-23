from rest_framework import serializers

from .models import Post

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

    class Meta:
        model = Post
        fields = (
            "id",
            "detalle_url",
            "uuid",
            "titulo",
            "cuerpo",
            "autor",
            "f_creacion",
            "f_actualizacion",
        )
