# Generated by Django 4.0.4 on 2022-05-15 06:46

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_accounts_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='email',
            field=models.CharField(max_length=45, unique=True, validators=[users.validators.validate_email]),
        ),
    ]