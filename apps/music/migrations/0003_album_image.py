# Generated by Django 4.1.12 on 2023-12-03 11:51

import apps.base.services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='image',
            field=models.ImageField(default=1, upload_to=apps.base.services.get_path_update_album),
            preserve_default=False,
        ),
    ]
