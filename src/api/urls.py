from django.urls import path, include

urlpatterns = [
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include('djoser.urls')),
]
