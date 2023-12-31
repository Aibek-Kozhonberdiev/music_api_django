# Generated by Django 4.1.12 on 2023-12-08 09:29

import apps.base.services
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_album_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='music',
            field=models.FileField(upload_to=apps.base.services.get_path_update_music, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])]),
        ),
    ]
