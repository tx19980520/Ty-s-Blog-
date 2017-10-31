"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.conf.urls.static import static
admin.autodiscover()
urlpatterns = [
    url(r'^admin/', admin.site.urls),#it is regex the second arguments
    url(r'^$',views.archive,),
    url(r'^blog/',views.blog,),
    url(r'^heartbeats/',views.heartbeats),
    url(r'^about/',views.about),
    url(r'^login/$', views.alogin),
    url(r'^logout/$',views.alogout),
    url(r'^register/$',views.register),
    url(r'^users/$',views.users),
    url(r'^detail/(.+)$',views.showdetail),
    url(r'^passwordchange/$',views.passwordchange),
    url(r'^avatarchange/$',views.avatarchange),
    url(r'^tags/(.*)/$',views.tags),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
