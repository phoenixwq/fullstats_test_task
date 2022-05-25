from django_filters.rest_framework import FilterSet, BooleanFilter
from rest_framework import filters
from .models import Post
from transliterate import translit


class PostFilterSet(FilterSet):
    like = BooleanFilter(method="get_liked")
    favorite = BooleanFilter(method="get_favorite")
    mine = BooleanFilter(method="get_mine")

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


class TranslitSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')
        params = params.replace(',', ' ')
        params = translit(params, "ru")
        return params.split()
