# Generated by Django 2.2.5 on 2021-09-21 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0035_auto_20210919_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='refund_limit_delta_hours',
            field=models.PositiveIntegerField(default=48),
        ),
    ]
