from rest_framework.routers import SimpleRouter
from django.urls import path
from posts.views import (
    PostView,
    MarkView,
    FavoriteView
)

router = SimpleRouter()
router.register("", PostView)

urlpatterns = [
    path('<int:post_pk>/marks/',
         MarkView.as_view(
             {
                 'get': 'list',
                 'post': 'create',
             })
         ),
    path('<int:post_pk>/marks/<int:pk>/',
         MarkView.as_view(
             {
                 'get': 'retrieve',
                 'put': 'update',
                 'delete': 'destroy'
             })
         ),
    path('<int:post_pk>/favorites/',
         FavoriteView.as_view(
             {
                 'get': 'list',
                 'post': 'create',
             })
         ),
    path('<int:post_pk>/favorites/<int:pk>/',
         FavoriteView.as_view(
             {
                 'get': 'retrieve',
                 'put': 'update',
                 'delete': 'destroy'
             })
         ),

]
urlpatterns += router.urls
