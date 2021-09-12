# Generated by Django 2.2.5 on 2021-06-19 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=600)),
                ('leader', models.CharField(max_length=64)),
                ('price', models.PositiveIntegerField(default=15)),
                ('duration', models.FloatField(default=3.5)),
                ('meetPlaceLink', models.CharField(default="https://www.google.com/maps/place/45%C2%B050'14.3%22N+11%C2%B044'11.2%22E/@45.8373125,11.7342488,17z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d45.8373125!4d11.7364375", max_length=600)),
                ('meetPlaceDirections', models.CharField(default='Verso Marostica ', max_length=600)),
                ('activityDetail', models.CharField(default='Andremo su per la collina e poi giu per la collina', max_length=600)),
                ('difficultyLevel', models.CharField(default='E', max_length=8)),
                ('length', models.FloatField(default=4)),
                ('gradient', models.FloatField(default=300)),
                ('streetType', models.CharField(default='Sterrato e asfalto', max_length=600)),
                ('whatToBring', models.CharField(default='Pranzo al sacco, acqua, crema solare, scarpe da trekking', max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, upload_to='TravelsApp/profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minNumPartecipants', models.PositiveIntegerField(default=10)),
                ('maxNumPartecipants', models.PositiveIntegerField(default=20)),
                ('confirmed', models.BooleanField(default=0)),
                ('dogsAllowed', models.BooleanField(default=0)),
                ('kidsAllowed', models.BooleanField(default=0)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TravelsApp.Activity')),
                ('partecipants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]