from django.db import models

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=45)
    phone = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Users'