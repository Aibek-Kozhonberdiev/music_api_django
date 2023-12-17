from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserLUDView)
router.register(r'profiles', views.ProfileCreateUpdateList)
router.register(r'favorites', views.FavoriteSetView)

urlpatterns = [
    path('user/', include(router.urls)),
    path('auth/create-user/', views.registration_user),
    path('auth/key-generate/', views.key_generate),
    path('auth/google-auth/', views.google_auth),
    path('auth/create-new-password/<int:pk>/', views.create_user_new_password),
]
