# Generated by Django 2.2.5 on 2021-08-06 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelsApp', '0026_auto_20210805_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_key',
            new_name='payment_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='chart', max_length=24),
        ),
    ]