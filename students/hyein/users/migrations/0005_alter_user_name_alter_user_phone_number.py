# Generated by Django 4.0.4 on 2022-05-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_name_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='', max_length=50),
        ),
    ]
