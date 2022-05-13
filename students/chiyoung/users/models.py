from django.db import models

class Accounts(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=45, unique= True) # How to deal with uppercase or lowercase ?
    password     = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=45)
    created_at   = models.DateTimeField(auto_now_add=True) # auto_now_add = True
    updated_at   = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'accounts'