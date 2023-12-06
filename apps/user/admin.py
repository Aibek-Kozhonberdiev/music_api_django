from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__username', )
    readonly_fields = ('user', )
    exclude = ('key', )


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ('id', 'content_type__model__icontains', )
