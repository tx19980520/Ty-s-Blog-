from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return self.title#now we choose the way from web, but I think the way book had is more beautiful

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='photo')
    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
class Article(models.Model):
    simple_production = models.CharField(max_length=200,default='')
    title= models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    Article_id = models.IntegerField()
    markdown = models.FileField(upload_to='article_markdown')
    def __str__(self):
        return self.title
