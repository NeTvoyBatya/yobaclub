# Generated by Django 3.2.9 on 2022-01-20 13:37

from django.db import migrations, models
import yobaclub.models


class Migration(migrations.Migration):

    dependencies = [
        ('yobaclub', '0015_auto_20220119_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinemaroom',
            name='waiting_users',
            field=models.TextField(default='[]', verbose_name="Messages in this room's chat"),
        ),
        migrations.AlterField(
            model_name='cinemaroom',
            name='room_id',
            field=models.CharField(default=yobaclub.models.create_hex, max_length=15, primary_key=True, serialize=False, unique=True, verbose_name='HEX-ID of the room'),
        ),
    ]
