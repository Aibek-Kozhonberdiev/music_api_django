# Generated by Django 4.1.12 on 2023-11-29 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]