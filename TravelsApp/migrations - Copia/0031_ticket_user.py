# Generated by Django 2.2.5 on 2021-08-13 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TravelsApp', '0030_remove_ticket_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.OneToOneField(default='flavio.bortolan@gmail.com', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]