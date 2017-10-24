from django.shortcuts import render
from blog.models import BlogPost
from django.views.decorators import csrf
from datetime import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
# Create your views here.
# Finally I choose to write normal html code in template and views just like back-end
def archive(request):
    return  render(request,'archive.html')
# Create your views here
def blog(request):
    if  not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.POST:
        bp = BlogPost()
        bp.title=request.POST['title']
        bp.body = request.POST['body']
        bp.timestamp = datetime.now()
        bp.save()
        posts = BlogPost.objects.all();
        return render(request, 'blog.html',{'posts':posts})
    else:
        posts = BlogPost.objects.all();
        return render(request, 'blog.html',{'posts':posts})
def about(request):
    return render(request,'about.html')
def heartbeats(request):
    if request.user.is_authenticated:
        return render(request,'heartbeats.html')
    else:
        return HttpResponseRedirect('/login')

#about log
def alogin(request):
    errors= []
    account=None
    password=None
    if request.method == 'POST' :
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password= request.POST.get('password')
        if account is not None and password is not None :
             user = auth.authenticate(username=account,password=password)
             if user is not None:
                 if user.is_active:
                     auth.login(request,user)
                     response= HttpResponseRedirect('/')
                     response.set_cookie('username',account,3600)
                     return HttpResponseRedirect('/')
                 else:
                     errors.append('disabled account')
             else :
                  errors.append('invaild user')
    return render(request, 'login.html',{'errors':errors})

def register(request):
    errors= []
    account=None
    password=None
    password2=None
    email=None
    CompareFlag=False
    avatar=None
    phone=None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password= request.POST.get('password')

        if not request.POST.get('phone'):
            errors.append('Please Enter phone')
        else:
            phone= request.POST.get('phone')

        if not request.POST.get('password2'):
            errors.append('Please Enter password2')
        else:
            password2= request.POST.get('password2')

        if not request.POST.get('email'):
            errors.append('Please Enter email')
        else:
            email= request.POST.get('email')

        if not request.POST.get('avatar'):
            errors.append('Please Enter your avatar')
        else:
            avatar = request.FILES.get('avatar')

        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else :
                errors.append('password2 is diff password')
                errors.append(password)
                errors.append(password2)
        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag :
            user=User.objects.create_user(account,email,password)
            user.is_active=True
            user.save
            return HttpResponseRedirect('/login')


    return render(request,'register.html',{'errors':errors})

def alogout(request):
    logout(request)
    return HttpResponseRedirect('/')
