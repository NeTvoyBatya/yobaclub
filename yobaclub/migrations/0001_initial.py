# Generated by Django 3.2.9 on 2021-12-12 10:42

from django.db import migrations, models
import yobaclub.logic.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='User ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='User Name')),
                ('mail', models.EmailField(max_length=254, unique=True, verbose_name='User Email')),
                ('password', models.CharField(max_length=200, verbose_name='User Passoword Hash')),
                ('registered_time', models.FloatField(default=yobaclub.logic.utils.models.get_current_timestamp, verbose_name='UTC Registration Date')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is user an admin')),
                ('is_vip', models.BooleanField(default=False, verbose_name='Is user an VIP')),
            ],
        ),
    ]
