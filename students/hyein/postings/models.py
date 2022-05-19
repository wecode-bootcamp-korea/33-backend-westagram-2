from django.db import models
from users.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    content    = models.CharField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        
class Image(models.Model):
    image = models.URLField(max_length=2000)
    post  = models.ForeignKey('post', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'images'