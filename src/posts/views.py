from django.contrib.auth import get_user_model
from posts.filters import PostFilterSet, TranslitSearchFilter
from posts.pagination import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from posts.permissions import IsAuthor
from posts.utils import save_post_visit
from rest_framework.response import Response
from posts.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    MarkSerializer,
    FavoriteSerializer,
)
from rest_framework import (
    mixins,
    generics,
    permissions,
    status,
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


class UserThroughPostBaseView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    model = None
    serializer_class = None
    permission_classes = (permissions.IsAuthenticated & IsAuthor,)

    def retrieve(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        instance = generics.get_object_or_404(self.model, user=request.user, post=post)
        serializer = self.get_serializer_class()(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        instance = generics.get_object_or_404(self.model, user=request.user, post=post)
        serializer = self.get_serializer_class()(instance, data=request.data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        instance = generics.get_object_or_404(self.model, user=request.user, post=post)
        serializer_data = self.get_serializer_class()(instance).data
        instance.delete()
        return Response(serializer_data, status=status.HTTP_200_OK)


class MarkView(UserThroughPostBaseView):
    serializer_class = MarkSerializer
    model = Mark


class FavoriteView(UserThroughPostBaseView):
    serializer_class = FavoriteSerializer
    model = Favorite
