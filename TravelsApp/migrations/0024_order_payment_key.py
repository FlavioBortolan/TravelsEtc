# Generated by Django 2.2.5 on 2021-08-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0023_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_key',
            field=models.CharField(default='xxx', max_length=200),
        ),
    ]
