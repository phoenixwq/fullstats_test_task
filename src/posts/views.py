from django.contrib.auth import get_user_model
from posts.filters import PostFilterSet, TranslitSearchFilter, UserPostActionFilter
from posts.pagination import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from posts.permissions import IsAuthor
from posts.utils import save_post_visit
from posts.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    MarkSerializer,
    FavoriteSerializer,
)
from rest_framework import (
    generics,
    permissions,
    filters,
    viewsets
)
from posts.models import (
    Post,
    Mark,
    Favorite
)

UserModel = get_user_model()


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        TranslitSearchFilter
    )
    filterset_class = PostFilterSet
    ordering_fields = ('created', 'visits', 'rating')
    search_fields = ('title',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly & IsAuthor,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        save_post_visit(request, instance)
        return super(PostView, self).retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class UserPostActionView(viewsets.ModelViewSet):
    model = None
    serializer_class = None
    permission_classes = (permissions.IsAuthenticated & IsAuthor,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserPostActionFilter

    def get_queryset(self):
        post = self.get_post()
        qs = self.model.objects.filter(post=post)
        return qs

    def get_object(self):
        pk = self.kwargs.get("pk")
        obj = generics.get_object_or_404(self.get_queryset(), pk=pk)
        return obj

    def get_post(self):
        post_pk = self.kwargs.get("post_pk")
        post = generics.get_object_or_404(Post, pk=post_pk)
        return post


class MarkView(UserPostActionView):
    serializer_class = MarkSerializer
    model = Mark


class FavoriteView(UserPostActionView):
    serializer_class = FavoriteSerializer
    model = Favorite
