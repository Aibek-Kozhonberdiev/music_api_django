from django.contrib import admin

from . import models


@admin.register(models.Podcast)
class AdminPodcast(admin.ModelAdmin):
    search_fields = ('id', 'title', 'user__username')
    readonly_fields = ('views', 'create_at')
