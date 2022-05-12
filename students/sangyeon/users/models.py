from django.db import models

class User(models.Model): 
    name         = models.CharField(max_length=50)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    create_at    = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = 'users'
# Create your models here.
