from django.db import models

class User(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    phone_number = models.IntegerField()

    class Meta:
        db_table = 'users'
# Create your models here.
