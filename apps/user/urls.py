from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserSetView)
router.register(r'profiles', views.ProfileSetView)

urlpatterns = [
    path('', include(router.urls)),
    path('create-user/', views.UserCreate.as_view()),
]
