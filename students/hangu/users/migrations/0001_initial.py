# Generated by Django 4.0.4 on 2022-05-13 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=45)),
                ('user_email', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=13)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
