from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'categories', views.CategorySetView)
router.register(r'musics', views.MusicSetView)

urlpatterns = [
    path('', include(router.urls)),
]
