from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryReadOnly)
router.register(r'musics', views.MusicSetView, basename='musics')
router.register(r'listen-music', views.MusicReadOnly, basename='listen-music')
router.register(r'albums', views.AlbumSetView)

urlpatterns = [
    path('', include(router.urls)),
]
