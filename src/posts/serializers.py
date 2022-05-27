from rest_framework import serializers
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from posts.models import (
    Post,
    Visit,
    Mark,
    Favorite
)
from django.db.utils import IntegrityError

UserModel = get_user_model()


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, default=serializers.CurrentUserDefault())
    rating = serializers.FloatField(read_only=True, default=0)
    created = serializers.DateTimeField(read_only=True)
    visits = serializers.IntegerField(
        read_only=True
    )
    likes = serializers.IntegerField(
        read_only=True
    )
    dislikes = serializers.IntegerField(
        read_only=True
    )
    visited = serializers.SerializerMethodField(method_name="is_visited")

    class Meta:
        model = Post
        exclude = ["users_favorites", "users_marks", "users_visits", "content"]

    def is_visited(self, obj) -> bool:
        request = self.context.get("request")
        if request.user.is_authenticated:
            return Visit.objects.filter(post=obj, user=request.user).exists()
        return False


class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        exclude = ["users_favorites", "users_marks", "users_visits"]


class UserThroughPostBaseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        required=False,
        write_only=True,
    )
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        try:
            instance = self.Meta.model.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("unique constraint post and user")
        return instance

    def update(self, instance, validated_data):
        post = validated_data.get("post")
        if instance.post != post:
            raise serializers.ValidationError("Can't change post!")
        return super(UserThroughPostBaseSerializer, self).update(instance, validated_data)

    class Meta:
        model = None


class MarkSerializer(UserThroughPostBaseSerializer):
    class Meta:
        model = Mark
        fields = "__all__"


class FavoriteSerializer(UserThroughPostBaseSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
