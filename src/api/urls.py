from django.urls import path, include

urlpatterns = [
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include('djoser.urls')),
    path('v1/posts/', include("posts.urls"))
]
