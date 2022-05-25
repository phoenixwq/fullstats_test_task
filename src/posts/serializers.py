from rest_framework import serializers
from .models import Post, Visit
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=serializers.CurrentUserDefault())
    rating = serializers.FloatField(read_only=True, default=0)
    created = serializers.DateTimeField(read_only=True)
    visits = serializers.IntegerField(
        source="get_visits_count",
        read_only=True
    )
    likes = serializers.IntegerField(
        source="get_likes_count",
        read_only=True
    )
    dislikes = serializers.IntegerField(
        source="get_dislikes_count",
        read_only=True
    )
    visited = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ["users_favorites", "users_marks", "users_visits", "content"]

    def get_visited(self, obj) -> bool:
        request = self.context.get("request")
        if request.user.is_authenticated:
            return Visit.objects.filter(post=obj, user=request.user).exists()
        return False


class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        exclude = ["users_favorites", "users_marks", "users_visits"]
