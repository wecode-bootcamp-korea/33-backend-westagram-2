from django.db import models

from users.models import User

class Posting(models.Model):
    title      = models.CharField(max_length=45, null=True)
    content    = models.CharField(max_length=300)
    image_url  = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'
    
class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    content    = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posting    = models.ForeignKey(Posting, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'comments'

class Like(models.Model):
    posting   = models.ForeignKey(Posting, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'



