# Generated by Django 3.2.11 on 2022-01-26 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yobaclub', '0020_cinemaroom_waiting_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_post',
            field=models.BooleanField(default=False, verbose_name='Can this user post video to group'),
        ),
    ]