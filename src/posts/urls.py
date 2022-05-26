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
    path('<int:pk>/mark/', MarkView.as_view(
        {
            'get': 'retrieve',
            "post": "create",
            "put": "update",
            "delete": "destroy"
        }
    )),
    path('<int:pk>/favorite/', FavoriteView.as_view(
        {
            'get': 'retrieve',
            "post": "create",
            "put": "update",
            "delete": "destroy"
        }
    ))

]
urlpatterns += router.urls
