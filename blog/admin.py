from django.contrib import admin
from blog import models
# Re-register UserAdmin
from blog.models import *
# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Comment)
