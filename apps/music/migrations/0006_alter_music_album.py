# Generated by Django 4.1.12 on 2023-11-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_remove_music_album_alter_music_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='album',
            field=models.ManyToManyField(blank=True, related_name='albums', to='music.album'),
        ),
    ]
