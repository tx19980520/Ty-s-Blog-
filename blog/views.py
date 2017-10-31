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
tail='''
<form action="" method='post'>
<div class='form-group'><label><font size='3px'>comment</font></label>
<input type='text' name="title" class='form-control' style='width:200px;' required><br>
</div>
</form>
</div><div class='col-md-2'>
</div>/<body></html>''' #I will add comment form here!
# Create your views here.
# Finally I choose to write normal html code in template and views just like back-end


def archive(request):
    return  render(request,'archive.html')
# Create your views here
def heartbeats(request):
    if  not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method=='POST':
        is_search=False
        if request.POST.has_key('search'):
            is_search = True
            words= request.POST['search']
            search_title=BlogPost.objects.filter(title__contains=words)
            search_body=BlogPost.objects.filter(body__contains=words)
            posts =search_body|search_title
            posts = list(posts)
            relation_people=[]
            for post in posts:
                b=User.objects.get(username=post.author)
                a=Profile.objects.get(user=b)
                relation_people.extend([a])
            posts = zip(posts,relation_people)
            return render(request,'heartbeats.html',{'posts':posts,'is_search':is_search,'word':words})
        if request.POST.has_key('body'):
            bp = BlogPost()
            bp.title=request.POST['title']
            bp.body = request.POST['body']
            bp.timestamp = datetime.now()
            bp.save()
            posts = BlogPost.objects.all();
            posts = list(posts)
            relation_people=[]
            for post in posts:
                b=User.objects.get(username=post.author)
                a=Profile.objects.get(user=b)
                relation_people.extend([a])
            posts = zip(posts,relation_people)
            return render(request, 'heartbeats.html',{'posts':posts,'is_search':is_search,'relation_people':relation_people})
    else:
        posts = BlogPost.objects.all();
        posts = list(posts)
        relation_people=[]
        for post in posts:
            b=User.objects.get(username=post.author)
            a=Profile.objects.get(user=b)
            relation_people.extend([a])
        posts = zip(posts,relation_people)
        return render(request, 'heartbeats.html',{'posts':posts,'relation_people':relation_people})

def about(request):
    return render(request,'about.html',)


def blog(request):
        istag = False
        if request.method =='POST':
            isfind = False
            if request.POST.has_key('search'):
                isfind=True
                word = request.POST['search']
                finds = Article.objects.filter(simple_production__contains=word)|Article.objects.filter(title__contains=word)|Article.objects.filter(author__contains=word)
                find = list(finds)
                paginator = Paginator(find, 3)
                page = request.GET.get('page')
                try:
                    find = paginator.page(page)
                    topics = find#Article.objects.all()[(int(page)-1)*3:int(page)*3]
                    ta =[]
                    for post in topics:
                        str = post.tags.split(" ")
                        ta.append(str)
                    topics = zip(topics,ta)
                    links = Article.objects.all()[:5]
                except PageNotAnInteger:
                    find = paginator.page(1)
                    if finds.count()>3:
                        topics = find[0:3]
                        ta =[]
                        for post in topics:
                            str = post.tags.split(" ")
                            ta.append(str)
                        topics = zip(topics,ta)
                        links = Article.objects.all()[:4]
                    else:
                        topics = find
                        ta =[]
                        for post in topics:
                            str = post.tags.split(" ")
                            ta.append(str)
                        topics = zip(topics,ta)
                        links = Article.objects.all()
                except EmptyPage:
                    print "e"
                    find = paginator.page(1)
                    topics = find
                    ta =[]
                    for post in topics:
                        str = post.tags.split(" ")
                        ta.append(str)
                    topics = zip(topics,ta)
                    links = Article.objects.all()
                return render(request,'blog.html',{'posts':find,'topic':topics,'links':links,'word':word,'isfind':isfind,"istag":istag})
            total=Article.objects.all().count()
            Article.objects.create(title=request.POST['title'],author=request.user.username,markdown=request.FILES.get('markdown'),simple_production=request.POST['simple_production'],Article_id=total+1,timestamp=datetime.now(),cover=request.FILES.get('cover'),tags=request.POST.get('tags'))
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
        posts = list(posts)
        paginator = Paginator(posts, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
            topics = Article.objects.all()[(int(page)-1)*3:int(page)*3]
            ta =[]
            for post in topics:
                str = post.tags.split(" ")
                ta.append(str)
            topics = zip(topics,ta)
            links = Article.objects.all()[:5]
        except PageNotAnInteger:
            posts = paginator.page(1)
            if Article.objects.all().count()>3:
                topics = Article.objects.all()[0:3]
                ta =[]
                for post in topics:
                    str = post.tags.split(" ")
                    ta.append(str)
                topics = zip(topics,ta)
                links = Article.objects.all()[:4]
            else:
                topics = Article.objects.all()
                ta =[]
                for post in topics:
                    str = post.tags.split(" ")
                    ta.append(str)
                topics = zip(topics,ta)
                links = Article.objects.all()
        except EmptyPage:
            print
            posts = paginator.page(paginator.num_pages)
            topics = Article.objects().all()[(paginator.num_pages-1)*3:paginator.num_pages*3+1]
            ta =[]
            for post in topics:
                str = post.tags.split(" ")
                ta.append(str)
            topics = zip(topics,ta)
        return render(request,'blog.html',{'posts':posts,'topic':topics,'links':links,"istag":istag})
#about log
def alogin(request):
    errors= []
    account=None
    password=None
    if request.method=='GET':
        return render(request, 'login.html',{'errors':errors})
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password= request.POST.get('password')
        if account is not None and password is not None :
            user = auth.authenticate(username=account, password=password)
            myuser = User.objects.get(username=account)
            check =myuser.check_password(password)
            if user and check:
                if user.is_active:
                    auth.login(request,user)
                    return render(request,'archive.html',)
                else:
                    errors.append("User is not active!")
                    return render(request,'login.html',{'errors':errors})
            else:
                errors.append("We don't have the user")
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
        if request.method=='GET':
            u = 'article'+str(num)+'.html'
            return render(request,u,)
        elif request.method=='POST':
            comment = comment.objects.create(witharticle=num,content=request.POST.get('comment'),)
    else:
        return HttpResponseRedirect('/login')
def users(request):
    if request.method == 'GET':
        try:
            myarticles=Article.objects.filter(author=request.user.username)
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
            m = User.objects.filter(username=request.user.username)
            m.set_password(password)
            m.save()
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

def tags(request,t):
    isfind = True
    istag = True
    search = Article.objects.filter(tags__contains=t)
    search = list(search)
    s = search
    paginator = Paginator(search, 3)
    page = request.GET.get('page')
    try:
        find = paginator.page(page)
        topics = search#Article.objects.all()[(int(page)-1)*3:int(page)*3]
        ta =[]
        for post in topics:
            str = post.tags.split(" ")
            ta.append(str)
        topics = zip(topics,ta)
        links = Article.objects.all()[:4]
    except PageNotAnInteger:
        find = paginator.page(1)
        if len(s)>3:
            topics = find[0:3]
            ta =[]
            for post in topics:
                str = post.tags.split(" ")
                ta.append(str)
            topics = zip(topics,ta)
            links = Article.objects.all()[:4]
        else:
            topics = find
            ta =[]
            for post in topics:
                str = post.tags.split(" ")
                ta.append(str)
            topics = zip(topics,ta)
            links = Article.objects.all()
    except EmptyPage:
        find = paginator.page(1)
        topics = find
        ta =[]
        for post in topics:
            str = post.tags.split(" ")
            ta.append(str)
        topics = zip(topics,ta)
        links = Article.objects.all()[:4]
    return render(request,'blog.html',{'posts':find,'topic':topics,'links':links,'word':t,'isfind':isfind,'istag':istag})
