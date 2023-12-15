from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryReadOnly)
router.register(r'listen-music', views.MusicReadOnly)
router.register(r'albums', views.AlbumSetView)
router.register(r'musics', views.MusicSetView)

urlpatterns = [
    path('', include(router.urls)),
]
