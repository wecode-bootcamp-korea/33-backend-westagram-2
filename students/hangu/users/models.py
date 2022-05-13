from django.db import models


class User(models.Model):
    user_name    = models.CharField(max_length=60)
    user_email   = models.CharField(max_length=60, unique=True)
    password     = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    created_at   = models.DateTimeField(auto_now_add=True, null=True)
    updated_at   = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'users'