import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render
from blog.models import BlogPost,Article,Profile
from django.views.decorators import csrf
from datetime import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
#from django.contrib.auth.decorators import login_required
import markdown
import codecs
from markdown.extensions import Extension
from markdown.util import etree
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
header='''
<!DOCTYPE html>
<html>
<head>
  <link rel='stylesheet' href='/static/css/code.css'>
  <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
  <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
  div.showimg {
    position: relative;
    top: -45px;
    left: 85px;
    width: 25px;
    height: 20px;
  }

  .avatarshow {
    width: 65px;
    height: 65px;
  }
</style>
<style>
  .carousel-inner img {
    width: 100%;
  }
</style>
<body>
  <div style='background:url(/static/image/homebg.jpg) !important;'>
    <br>
    <div>
      <nav>
        <div class="row">
          <font color='white' size='7px'>&thinsp;&thinsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xiao Tan</font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <font color='white' size='4px'>Practice curves is always <b>e<sup>x</sup></b></font>
          <div style='float:right'>
            {% if request.user.is_authenticated %}
            <ul class='navbar'>
              <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#"></a>
                <font color='#337ab7' size='3px'><b>Welcome!&nbsp;&nbsp;{{user.username}}</b></font><b class="caret"></b></a>&thinsp;&thinsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <ul class="dropdown-menu">
                  <li>
                    <a href='/logout'>logout</a>
                  </li>
                </ul>
            </ul>
            <div class='showimg'>
              <img class='avatarshow img-circle' src='{{request.user.profile.avatar.url}}' ,alt='{{request.user.profile.phone}}'>
            </div>
            {% else %}
            <ul class='navbar'>
              <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#"></a>
                <font color='#337ab7' size='3px'><b>Welcome!&nbsp;&nbsp;guy!</b></font><b class="caret"></b></a>&thinsp;&thinsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <ul class="dropdown-menu">
                  <li>
                    <a href='/login'>login</a>
                  </li>
                  <li>
                    <a href='/register'>register</a>
                  </li>
                </ul>
            </ul>
            {% endif %}
          </div>
          <div class="span8" style='float:right'>
            <br>
            <ul class="nav nav-pills">
              <li><a href="/"><b style='font-size:18px'>Home</b></a></li>
              <li class='active'><a href="/blog"><b style='font-size:18px'>Blog</b></a></li>
              <li><a href="https://github.com/tx19980520"><b style='font-size:18px'>GitHub</b></a></li>
              <li><a href="/about"><b style='font-size:18px'>About</b></a></li>
              <li><a href='/heartbeats'><b style='font-size:18px'>Heart Beats</b></a></li>
            </ul>
          </div>
        </div>
      </nav>
      <p class='text-center'>
        <label class='text-center'><font color='white' size='4px'>For more Technology</font></label><br>
        <label class="text-center"><font color='white' size='4px'>technical otaku Save the world</font></label>
      </p>
    </div>
  </div>
  <div class='col-md-2'></div>
<div class='col-md-8'>
    '''
tail='''</div><div class='col-md-2'>
</div>/<body></html>'''
# Create your views here.
# Finally I choose to write normal html code in template and views just like back-end


def archive(request):
    return  render(request,'archive.html')
# Create your views here
def heartbeats(request):
    if  not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.POST:
        bp = BlogPost()
        bp.title=request.POST['title']
        bp.body = request.POST['body']
        bp.timestamp = datetime.now()
        bp.save()
        posts = BlogPost.objects.all();
        return render(request, 'heartbeats.html',{'posts':posts})
    else:
        posts = BlogPost.objects.all();
        return render(request, 'heartbeats.html',{'posts':posts})

def about(request):
    return render(request,'about.html',)


def blog(request):
        if request.method =='POST':
            total=Article.objects.all().count()
            Article.objects.create(title=request.POST['title'],author=request.user.username,markdown=request.FILES.get('markdown'),simple_production=request.POST['simple_production'],Article_id=total+1,timestamp=datetime.now())
            goal =Article.objects.get(Article_id=total+1)
            input_file = codecs.open(settings.BASE_DIR+goal.markdown.url,'r',encoding='utf-8')
            text=input_file.read()
            html = markdown.markdown(text,extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
            input_file.close()
            newhtml = codecs.open(settings.BASE_DIR+r'/blog/templates/article'+str(total+1)+'.html','w',encoding='utf-8')
            newhtml.write(header)
            newhtml.write(html)
            newhtml.write(tail)
            newhtml.close()
            posts = Article.objects.all()
            return render(request,'blog.html',{'posts':posts})
        if request.method=='GET':
            posts = Article.objects.all()
            paginator = Paginator(posts, 3)
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
                topics = Article.objects.all()[(int(page)-1)*3:int(page)*3]
                links = Article.objects.all()[:5]
            except PageNotAnInteger:
                posts = paginator.page(1)
                if Article.objects.all().count()>3:
                    topics = Article.objects.all()[0:3]
                    links = Article.objects.all()[:4]
                else:
                    topics = Article.objects.all()
                    links = Article.objects.all()
            except EmptyPage:
                posts = paginator.page(pageinator.num_pages)
                topics = Article.objects().all()[(pageinator.num_page-1)*3:pageinator.num_pages*3+1]
            return render(request,'blog.html',{'posts':posts,'topic':topics,'links':links})
#about log
def alogin(request):
    errors= []
    account=None
    password=None
    request.session['login_from'] = '/blog'
    if request.method=='GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        if request.session['login_from'] == '/':
            request.session['login_from'] = '/blog'
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
            try:
                user = User.objects.get(username=account,password=password)#for check the name and the password
            except ObjectDoesNotExist:
                errors.append('invaild user')
                return render(request, 'login.html',{'errors':errors})
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    return HttpResponseRedirect(request.session['login_from'])# for  redirect to previous web
            else:
                return render(request,'archive.html')
    return render(request, 'login.html',{'errors':errors})

def register(request):
    errors= []
    account=None
    password=None
    password2=None
    email=None
    CompareFlag=False
    avatar=False
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

        if not request.FILES.get('avatar'):
            errors.append('Please Enter your avatar')
        else:
            avatar = True

        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else :
                errors.append('password2 is diff password')
        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag and avatar :
            user=User.objects.create(username=account,password=password,email=email)
            user.is_active=True
            user.save
            num = User.objects.all().count()
            profile = Profile.objects.create(user=user,avatar=request.FILES.get('avatar'),phone=phone,idnumber=num)
            profile.save
            return HttpResponseRedirect('/login')


    return render(request,'register.html',{'errors':errors})

def alogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def showdetail(request,num):
    if request.user.is_authenticated:
        u = 'article'+str(num)+'.html'
        if request.method=='GET':
            return render(request,u)
    else:
        return HttpResponseRedirect('/login')
def users(request):
    if request.method == 'GET':
        try:
            myarticles = Article.objects.get(author=request.user.username)
        except ObjectDoesNotExist:
            myarticles = []
        return render(request,'users.html',{'myarticles':myarticles})
def passwordchange(request):
    if request.method=='GET':
        return render(request,'password.html')
    elif request.method=='POST':
        errors= []
        password=None
        password2=None
        CompareFlag=False
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password= request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('Please Enter password2')
        else:
            password2= request.POST.get('password2')
        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else :
                errors.append('password2 is diff password')
        if password is not None and password2 is not None and CompareFlag :
            User.objects.filter(username=request.user.username).update(password=password)
            return HttpResponseRedirect('/login')
def avatarchange(request):
    if request.method == 'POST':
        avatar = request.FILES.get('new_avatar')
        name = avatar.name
        print name
        totalname = settings.MEDIA_ROOT+'/photo/'+name;
        with open(totalname, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        pro = Profile.objects.filter(idnumber=request.user.profile.idnumber).update(avatar=totalname)
        return HttpResponseRedirect('/')
    elif request.method == 'GET':
        return render(request,'avatarchange.html')
