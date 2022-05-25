from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .filters import PostFilterSet
from .models import Post
from .pagination import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
)

UserModel = get_user_model()


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PostFilterSet
    ordering_fields = ('created', 'visits', 'rating')

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
