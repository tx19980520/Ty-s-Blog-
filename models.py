from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return self.title#now we choose the way from web, but I think the way book had is more beautiful

class MyUser(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='photo')
    def __str__(self):
        return self.phone

def create_user_MyUser(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = MyUser()
        profile.user = instance
        profile.save()
