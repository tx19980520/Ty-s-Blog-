from django.contrib import admin
from blog import models
# Re-register UserAdmin
admin.site.register(models.MyUser)
admin.site.register(models.BlogPost)
