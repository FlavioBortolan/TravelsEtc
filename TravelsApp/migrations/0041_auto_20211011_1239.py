# Generated by Django 2.2.5 on 2021-10-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0040_auto_20211009_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activityDetail',
            field=models.CharField(default='xxxxxxxxxxxxxxxxxx', max_length=2048),
        ),
    ]
