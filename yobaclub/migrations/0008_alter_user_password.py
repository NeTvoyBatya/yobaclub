# Generated by Django 3.2.9 on 2022-01-03 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yobaclub', '0007_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=2000, verbose_name='User Password Hash'),
        ),
    ]
