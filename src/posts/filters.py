from django_filters import rest_framework as filters
from .models import Post


class PostFilterSet(filters.FilterSet):
    like = filters.BooleanFilter(method="get_liked")
    favorite = filters.BooleanFilter(method="get_favorite")
    mine = filters.BooleanFilter(method="get_mine")

    def get_favorite(self, queryset, field_name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(users_favorites=user)
        return queryset

    def get_mine(self, queryset, field_name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(author=user)
        return queryset

    def get_liked(self, queryset, field_name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(mark__value=1)
        return queryset

    class Meta:
        model = Post
        fields = ["favorite", "like", "mine"]

