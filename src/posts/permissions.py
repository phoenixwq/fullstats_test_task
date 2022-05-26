from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from posts.models import Post


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            if isinstance(obj, Post):
                return request.user == obj.author
            else:
                return request.user == obj.user
        return True

