# Generated by Django 2.2.5 on 2021-07-19 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0012_userprofileinfo_user_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='dateTime',
            new_name='date',
        ),
    ]
