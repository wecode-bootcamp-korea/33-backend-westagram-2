from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=10)
    user_email = models.CharField(max_length=45)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)

    class Meta:
        db_tables = 'user'