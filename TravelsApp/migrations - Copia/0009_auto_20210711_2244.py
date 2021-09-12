# Generated by Django 2.2.5 on 2021-07-11 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0008_userprofileinfo_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='credits',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='phone_number',
            field=models.CharField(blank=True, max_length=64, validators=[django.core.validators.RegexValidator(message='Phone number must be entered like: 340 1461538. Up to 10 digits allowed. Only digits, no other character allowed.', regex='^(( *0 *0 *| *\\+) *3 *9 *)?((\\d *){3})((\\d *){6,7})$')]),
        ),
    ]