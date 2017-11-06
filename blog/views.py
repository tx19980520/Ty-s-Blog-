import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render
from blog.models import BlogPost,Article,Profile,Comment
from django.views.decorators import csrf
from datetime import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout
import re
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
<link rel="icon" sizes="any" mask href="http://www.cqdulux.cn/media/favicon.ico">
  <link rel='stylesheet' href='/static/css/code.css'>
  <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  <script src="/static/javascript/article.js"></script>
  <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
  <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
.nav{
  position:absolute;
  top:43px;
  right:233px;
}
.top{
  position:absolute;
  top:20px;
  right:66.3px;
}
h1{
  text-align:center
}
.sidebar {
  position: fixed;
  padding-left: 10px;

  border-left: solid;
  border-color: black;
  border-width: 2px;
}
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
  .showcover {
  float: left;
  width: 200px;
  height: 150px;
  margin: 5px;
}
  .carousel-inner img {
    width: 100%;
  }
</style>
<body>
  <div style="background:url(/static/image/homebg.jpg)">
    <br>
    <div>
      <nav>
        <div class="row">
          <font color='white' size='7px'>&thinsp;&thinsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Xiao Tan</font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <font color='white' size='4px'>Practice curves is always <b>e<sup>x</sup></b></font>
          <div class="top">
            {% if request.user.is_authenticated %}
            <ul class='navbar'>
              <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                  <font color='#337ab7' size='3px'><b>{{user.username}}</b></font>
                  <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li>
                    <a href='/logout'>logout</a>
                  </li>
                  <li>
                    <a href='/users'>your imformation</a>
                  </li>
                </ul>
              </li>
            </ul>
            <div class='showimg'>
              <img class='avatarshow img-circle' src='{{request.user.profile.avatar.url}}' ,alt='{{request.user.profile.phone}}'>
            </div>
            {% else %}
            <ul class='navbar'>
              <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                  <font color='white' size='3px'><b>Welcome!&nbsp;&nbsp;guy!</b></font>
                  <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li>
                    <a href='/login?next={{request.path}}'>login</a>
                  </li>
                  <li>
                    <a href='/register'>register</a>
                  </li>
                </ul>
              </li>
            </ul>
            {% endif %}
          </div>
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
      <br>
      <p class='text-center'>
        <label class='text-center'><font color='white' size='4px'>For more Technology</font></label><br>
        <label class="text-center"><font color='white' size='4px'>Technical otaku save the world</font></label>
      </p>
      </div>
    </div>
  </div>
    <div class='col-md-1'></div>
<div class='col-md-8 panel panel-default'>
  <div class="panel-body">
    '''
tail='''
<br>
<br>
<br>
<br>
<br>
<br>
<br>
{% if hascomment %}
<p><font size="5px;">Comments</font></p>
{% for com in comments %}
<p><font>{{forloop.counter}}
{{com.0.author}} &nbsp;&nbsp;&nbsp;&nbsp;<button class="btn btn-default" onclick="reply({{forloop.counter}})">reply</button>
</p>
<img src="{{com.1}}" class="avatarshow img-circle" style="position:relative;float:left;">
<p style="margin-left:75px;"><font size="3x;">{{com.0.content}}</font></p>
<br>
<br>
<time style="float:left;">{{com.0.timestamp}}</time>
<hr style="height:2px;border:none;border-top:2px;background-color:black;">
{% endfor %}
{% endif %}
<form action="" method='post'>
{% csrf_token %}
<div class='form-group'><label><font size='3px'>comment</font></label>
<textarea type='text' id="editcomment" name='editcomment' onblur="checkcomment()" class='form-control' rows="3" required></textarea><br>
</div>
<p class='text-center'>
  {% if request.user.is_authenticated %}
  <button type="submit" value="submit" class='btn btn-default'>comment</button>
  {% else %}
  <p class="text-center"><font size="3px">If you wanna post,login first!</font></p>
  {% endif %}
</p>
</form>
{% endif %}</div></div>
<div class="col-md-3">
  <aside>
    <div class="sidebar">
      <font size='2.5px'>
          <font size='4px'>Others the author has</font>
        </p>
        {% for link in links %}
        <p>
          <a href='/detail/{{link.Article_id}}'>
            {{link.title}}</a>
        </p>
        {% endfor %}
        </font>
      </font>
    </div>
  </aside>
</div>
</body>
</html>
''' #I will add comment form here!
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
            bp.author= request.user.username
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
                paginator = Paginator(find, 5)
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
                    if finds.count()>4:
                        topics = find[0:5]
                        ta =[]
                        for post in topics:
                            str = post.tags.split(" ")
                            ta.append(str)
                        topics = zip(topics,ta)
                        links = Article.objects.all()[:5]
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
                    links = Article.objects.all()
                return render(request,'blog.html',{'posts':find,'topic':topics,'links':links,'word':word,'isfind':isfind,"istag":istag})
            total=Article.objects.all().count()
            if (request.FILES.get('markdown').size/1000/1024)>10000:
                return render(request,"archive.html")

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
            newhtml = codecs.open(settings.BASE_DIR+r'/blog/templates/article%d.html'%(total+1),'w',encoding='utf-8')
            newhtml.write(header)
            newhtml.write(html)
            newhtml.write(tail)
            newhtml.close()

        posts = Article.objects.all()
        posts = list(posts)
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
            topics = Article.objects.all()[(int(page)-1)*5:int(page)*5]
            ta =[]
            for post in topics:
                strs = post.tags.split(" ")
                ta.append(strs)
            topics = zip(topics,ta)
            links = Article.objects.all()[:5]
        except PageNotAnInteger:
            posts = paginator.page(1)
            if Article.objects.all().count()>4:
                topics = Article.objects.all()[0:4]
                ta =[]
                for post in topics:
                    strs = post.tags.split(" ")
                    ta.append(strs)
                topics = zip(topics,ta)
                links = Article.objects.all()[:4]
            else:
                topics = Article.objects.all()
                ta =[]
                for post in topics:
                    strs = post.tags.split(" ")
                    ta.append(strs)
                topics = zip(topics,ta)
                links = Article.objects.all()
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            topics = Article.objects().all()[(paginator.num_pages-1)*4:paginator.num_pages*4+1]
            ta =[]
            for post in topics:
                strs = post.tags.split(" ")
                ta.append(strs)
            topics = zip(topics,ta)
        return render(request,'blog.html',{'posts':posts,'topic':topics,'links':links,"istag":istag})
#about log
def alogin(request):
    errors= []
    account=None
    password=None
    if request.method=='GET':
        pre_web = request.GET.get('next')
        return render(request, 'login.html',{'errors':errors,"next":pre_web})
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
            myuser = User.objects.get(username=account)
            check = False
            if myuser.password == password:
                check = True
            if check:
                if myuser.is_active:
                    auth.login(request,myuser)
                    pre_web = request.POST.get('next')
                    if pre_web == 'None':
                        return render(request,"archive.html")
                    return redirect(pre_web)
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
    size = True
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
        if (request.FILES.get('avatar').size/1024/1024)>2:
            size = false;
            erros.append('your avatar file is too big to upload!')
        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag and avatar and size :
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
    if request.method=='GET':
        hascomment = True
        url = 'article'+str(num)+'.html'
        tauthor = Article.objects.get(Article_id=num).author
        links = Article.objects.filter(author=tauthor)
        comments=Comment.objects.filter(witharticle=num).order_by('floor')
        comments = list(comments)
        if len(comments)>=1:
            hascomment = True
            avatars=[]
            for c in comments:
                user = User.objects.get(username=c.author)
                profile = Profile.objects.get(user=user)
                avatars.append(profile.avatar.url)
            comments = zip(comments,avatars)
        return render(request,url,{"comments":comments,"hascomment":hascomment,"links":links})
    elif request.method=='POST':
        tauthor = Article.objects.get(Article_id=num).author
        links = Article.objects.filter(author=tauthor)
        hascomment = True
        cont = request.POST['editcomment']
        go = re.match('reply num (.+):',cont)
        if go == None:
            getfloor = Comment.objects.filter(witharticle=num).count()+1
            Comment.objects.create(witharticle=num,content=request.POST.get('editcomment'),floor=getfloor,father=0,author=request.user.username)
        elif go != None:
            father = int(go.group(1))
            getfloor = Comment.objects.filter(witharticle=num).count()+1
            Comment.objects.create(witharticle=num,content=request.POST.get('editcomment'),floor=getfloor,father=father,author=request.user.username)
        url = 'article'+str(num)+'.html'
        comments=Comment.objects.filter(witharticle=num).order_by('floor')
        comments = list(comments)
        avatars=[]
        for c in comments:
            user = User.objects.get(username=c.author)
            profile = Profile.objects.get(user=user)
            avatars.append(profile.avatar.url)
        comments = zip(comments,avatars)
        if len(comments)>=1:
            hascomment = True
        return render(request,url,{"comments":comments,"hascomment":hascomment,"links":links})
def users(request):
    if request.method == 'GET':
        try:
            t=[]
            myarticles=Article.objects.filter(author=request.user.username).order_by("timestamp")
            myarticles = list(myarticles)
            for a in myarticles:
                strs = a.tags.split(" ")
                t.append(strs)
            myarticles = zip(myarticles,t)
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
        totalname = settings.MEDIA_ROOT+"/photo/"+name
        with open(totalname, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        totalname = "/photo/"+name
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
