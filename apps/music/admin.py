from django.contrib import admin

from . import models

admin.site.register(models.Music)
admin.site.register(models.Category)
