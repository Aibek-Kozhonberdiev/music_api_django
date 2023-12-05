from django.contrib import admin

from . import models


@admin.register(models.Music)
class MusicAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', 'user__username')
    readonly_fields = ('views', 'create')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', )


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', 'author__username')
    readonly_fields = ('create', )
