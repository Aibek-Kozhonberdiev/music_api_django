from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'categories', views.CategorySetView)
router.register(r'musics', views.MusicSetView)
router.register(r'albums', views.AlbumSetView)

urlpatterns = [
    path('', include(router.urls)),
]
