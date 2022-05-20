from django.db import models


class User(models.Model):
    user_name      = models.CharField(max_length=60)
    user_email     = models.CharField(max_length=60, unique=True)
    password       = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=13)
    created_at     = models.DateTimeField(auto_now_add=True, null=True)
    updated_at     = models.DateTimeField(auto_now=True, null=True)
    followfollwing = models.ManyToManyField('self', symmetrical=False, through='FollowFollowing')

    class Meta:
        db_table = 'users'

class FollowFollowing(models.Model):
    follow_user    = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='following_user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'followsfollowings'
