# Generated by Django 4.0.4 on 2022-05-18 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0002_alter_image_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='posting',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]