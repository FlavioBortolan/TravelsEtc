# Generated by Django 2.2.5 on 2021-10-08 23:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0037_auto_20210923_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='partecipants',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
