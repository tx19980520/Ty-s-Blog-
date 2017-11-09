# 基于Django1.11.6个人博客开发后期总结

##Django1.11.6项目简介

首先必须强调的是我是1.11.6的版本，其他版本是什么样子我一概不知，我也是在网上找博文然后学习的，其次我只保证按我说的去做一定会实现，但如果有更好的实现方法那你自行百度。

想要看大段代码的点击下面的链接

https://github.com/tx19980520/Ty-s-Blog-

整个框架有几个很重要的基本文档，我给大家简单梳理一下：

1. manage.py

   这个文档你可以简单的理解为一个指令库，在命令行界面（主意这里不是指的python的命令行界面，是系统的）操作，对整个框架进行调整，暂时你记得如下的几个操作就好，注意，使用下列指令是的命令行路径一定是要在manage.py的path。

   ```python
   manage.py runserver
   #模拟执行服务器运行，在浏览器中使用127.0.0.1可以对你的网页进行访问
   manage.py makemigrations
   manage.py migrate
   #如果你不懂不要紧，你只需要知道在每次你修改完你的models.py文档后把这两个命令按先后顺序输入就好
   manage.py createsuperuser
   #创建一个超级用户，这指令输出后会让你填写一些基本信息
   manage.py startproject xxx
   #创建一个项目创建之后会在manage.py下生成一系列文件。
   manage.py startapp yyy
   #但是记得创建之后还是得在settings里面去设置（后面我会讲到）
   ```

   ​

2. settings.py

   这个文档是掌控整个项目的结构的，新手入门的话你只需要注意以下的地方

   ```
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   #相当于是储存一个你项目的所在地
   INSTALLED_APPS =[]
   #django把每一个具体的项目（或者叫板块？）都定义为一个app，你之后会使用一个指令创建一个app，然后在这里手动添加其名字
   DATABASE=｛｝
   #这个地方主要是对于后台数据库的一个基本信息的填写，默认为sqlite3，你如果要改成mysql之类的数据库的话可以在网上自行百度，这个方面其余博客讲的没有语法错误
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   #上两行设置的是你的本地服务器里面储存上传文件的地方会和后面的一个up_load配合使用
   STATIC_URL = '/static/'
   STATICFILES_DIRS = (
       os.path.join(BASE_DIR, "static"),
   #上两行设置的是你的本地服务器里面储存静态的一些图片和css，便于你后面添加到你的html中进行美化
   )
   ```

   ​


3. urls.py

这个文件只有一个用途，他只有一个函数。下面节选自我代码中的一段

```python
urlpatterns = [
    url(r'^detail/(.+)$',views.showdetail,name="sdsdaqdsa"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

首先url的第一个参数是一个正则表达，正则括号提取的东西会自动传到第二个参数——一个函数中去，当然你要在函数声明中写一个形式参数来表示它，最后的这个name如果各位能够理解的话可以使用，前面的正则是显现在地址栏里面给用户看的，如果我们在html里面写```<a href='/detail/1'>```这样的话如果我们想更改正则，我们得把所用用到的地方都给了，但是如果我们取一个相对固定的别名从别名找到这个地址，这就很简单了，这个地方具体实现的函数我们后面的重定义的地方写

最后那个加号后面的是为了告诉项目，咱在后面讲到的一切地方的/media都是指的我们之前定义的那个地方。

4. views.py

   这个地方接着讲上面的views.showdetail是什么，如果你之前部署过一个网站，不是用的这个框架，而是PHP之类的语言，你会知道有一个根目录的理解方式，那当然也非常的简单易懂，但这里django提出的方式是，使用正则匹配，匹配到对应的函数，至于反给你什么界面，做了什么操作，全看这个函数的写法。在你的app文件夹下面会存在有一个templates这个文件夹，如果没有你自己建，使用这样的调用方式，就可以把所有的html文件放置在该文件夹下（注，我不用django表单，这可能不是很拥抱这个框架，但是我觉得写正常表单在html中更加的明了）

5. models

   顾名思义models是定义你的一些模型，这些模型都会放进你的数据库，为了方面记得定义str函数，之后我们会讲这有什么用。基本的板子如下：

   ```python
   class BlogPost(models.Model):
       title = models.CharField(max_length=150)
       author = models.CharField(max_length=50,default='admin')
       body = models.TextField()
       timestamp = models.DateTimeField()
       def __str__(self):
           return self.title
   ```

   models.xxxxFiled()是创建各类元素的方式，这个地方强调下，default是如果没有的情况默认存在的值，记得这个值得和你定义的元素是一类的，不要定义个整数然后你去```default=''```这就会报错，当然如果你忘记了添加该项或者是```null=True```这一项，你在处理数据的时候会提醒你，并让你做出选择。

   我们这个地方要讲，我们要建立类和类之间的关系这里的关系有一对一（OnetoOneField）、一对多（ForeignKey）、多对多（ManyToManyField），这个地方我承认我的代码写丑了，我的博客里面的Comments和Article和User的关系没有写出来，这导致的是我在后端处理的时候使用数据库搜索的次数非常多，如果是一个大型网站，那么多次调用数据库很容易导致用电过高或者服务器的崩溃。

   我们之前学习过python的同学可以简单的把OneToOneField理解为在新定义的类中去添加一个原来定义的类，ForeignKey和ManyToManyField部分是建立数据库关系的重要部分，具体的语法你可以在一下的网站中习得：http://www.cnblogs.com/linxiyue/p/3667418.html，数据库操作水平高的同学会觉得这很方便。

   可以先讲一下我这网站中暂时用到的仅有的一次OneToOneField，是为了扩展本有的User，这也是其主要的功能，贴一下代码：

   ```python
   class Profile(models.Model):
       user = models.OneToOneField(User, on_delete=models.CASCADE)
       idnumber = models.IntegerField(default=1)
       phone = models.CharField(max_length=30)
       avatar = models.ImageField(upload_to='photo')
   #upload_to='photo'指的是你创建这个ImageField上传储存在/media/photo的目录里面，第一次上传会自动生成该文件夹
       def __str__(self):
           return self.user.username
   ```

   我们扩展了几个方面，主要是为了头像的添加。

6. admin.py

   这个文件里面就一个函数是必须的，可能你在各个地方告诉过你一些优异的register的方式，我只讲最朴素的，直接register，只有一个参数，参数是你在models.py里面定义的class。

   register的目的都是为了一个东西，django自带的admin页面，你可以使用之前注册过的superuser到127.0.0.1/admin登陆进入页面，可以看到一个管理页面，是管理后台数据的（如果你用过PHPmyAdmin会觉得基本是一个套路，只不过更加的友善了

   简单的框架旧式这样具体的函数坑我们后面来讲

## python与HTML的结合

简单的讲我们html是静态的界面，我们需要用python（为了用户友好还是得用JS）去显示一些数据库调出来的东西，view.py的具体函数会在传回页面的时候传回一些参数供页面使用（具体怎么传，后面来讲）

这里的具体语法我推荐这篇博客说的，至少是没错的，另外我不推荐一切的django表单，因为如果要改框架或语言，这似乎不太方便（当然这也让我一定程度上不去拥抱django框架）

不要在html里面写太多的东西，最好是后台把东西都处理好了让前端简单处理下输出即可

注意如果你要传值给js在传值的时候需要特殊化处理，这个后面再讲。

## 用python建立后台

###基本的view函数

我们的后端基本就是整个view.py，在这里面定义的每一个函数对应着一个或者一个系列的页面的处理。我给出一个最基本的模板代码：

```python
def about(request):#request是默认的必带函数，说明你是接受了请求，这个请求会带回给后端一些必要的数据
    return render(request,'about.html',)

```

这是最简单的view函数，什么都不处理，直接返回一个页面。

###view函数的丰富

我们不可能只是单独返回一个html文档，那真的是十分的单调。

#### 重定向的方式的丰富

首先我们丰富我们返回一个页面的方式，有如下几个方法，

```python
render(request,template,{})
#render函数有三个参数，第一个依旧是request，带着原请求的一些记录与信息进入新的页面，template是templates文件夹的的某个html文件，最后还有一个参数是一个字典，你可能在后端处理好了一些数据你要展现在前端，我们就通过这个字典传值到前端进行部署，最后一个参数也可以改为local()，相当于把该函数里面生成的所有对象对传给前端。还有render_to_response(),你可以理解为老板的render，render参数写法更让人觉得舒服
HttpResponseRedirect("/")
#HttpResponseRedirect这个函数是直接重定义到你输入的字符串正则匹配的页面，通过在?x=2这种方式传值，但是会觉得很不明显，对你开发不是很友好。
#redict有一下几个用法
redict(model.object)
#传给redict一个具体的对象，这个对象的类得定义了get_absolute_url()返回一个具体的字符串，重定义到具体的页面。
def get_absolute_url(self):
    return "/people/%i/" % self.id
#我们就重定向"/people/self.id/"
redict("some-view-name",*agrs)
#我们先介绍另外的一个函数
reverse("some-view-name")
#我们之前提到过我们在urls.py定义name的问题，通过reverse函数返回对应name的url
#所以redict的第二种用法里的第一个参数是reverse的参数，后面的args是一个元组，你可以传递一些参数给这个页面
redict("/some/s")
#第三种法相当于给出reverse之后的结果，通过urls.py的正则直接重定向
redict("https://www.baidu.com")
#第四种直接给网址当然是可以的，只不过只是网站内部跳转的话，这样显得很蠢

```

对于萌新来讲我推荐使用render，参数的表达显而易见，萌新也是做小项目，要是真的改了正则匹配，要改的地方也不会太多，而且调试的时候肯定会报错，所以使用redict的意义不是太大。但redict(model.object)这个用法让人觉得非常的舒服，具有没学，比如你的Article类里面每一个文章都对应了一个文章html网页，这个网页是article+id.html，id是你文章的编号，那你完全可以在类里面把这个东西处理好，直接返回给view层面，非常的简洁。

####数据库与python

如果你熟悉python的话，我们如果得到了数据你在view的函数里面处理即可，我们要获取数据，就是从数据库里面去提取数据，这个地方我们不需要去专门学习SQL的专门的语法，只要你在settings.py文档中写清楚了你的数据库信息，你可以直接调用python的函数去获得一些数据对象，下面简介一下各函数：

```python
我们的对象暂定为
class people(models.model):
  name = CharField(max_length=150,null=True)
  id = IntegerField(default=1)
添加对象：
people.objects.create(name="Amy",id=1)
#id可以不写，那么默认为1
得到对象：
people.objects.all()
#得到所有的对象
people.objects.get(name="Amy")
people.objects.filter(name__contains="A")
#这个地方有一个坑，get只会返回一个数据，filter会返回一个set，主义这个地方返会的对象是set，如果你想按顺序遍历，你需要使用list()进行转换
#你如果了解数据库的相关知识你会知道我们的搜索方式不止一种，甚至是正则匹配，我们一下会给出一个网站，里面的相关字段会给出得比较全，这种东西随查随用。
修改对象：
people.objects.get(name="Amy").update(id = 5)
删除对象：
people.objects.get(name="Amy").delete()
排序：
people.objects.all().order_by(name,)
#首先强调，这个排序可以有多个字段，重要程度按函数参数顺序递减，字符串的比较是按位比较ascii码
```

注意一定要少用数据库查询，在大数据的情况下这样的代价是真的不能忽视的。

我之后在寒假会重构该部分，把几个model的关系写清楚

#### view代码中文件的问题

这个问题出现的主要原因是我在添加avatar元素的时候发生的一系列问题，我在用户注册的时候的avatar上传出现了一些坑我们一个一个来题说：

1. 图片的显示

显示图片很简单，我们html的标签里面有img标签，src我却不知道怎么写，后来进行无数种可能的尝试之后终于得出结论，在django项目的app中，都是以appname的文件夹为根目录，我们默认存储的地方是media/photo，media是默认的储存上传文件的地址。我之前会觉得我是不是还要存储一个字符串来记录其地址，后来发现你可以直接调用avatar.url来得到上传的静态文件的url你可以直接写在img标签的src="{{profile.avatar.url}}"

注意一下div和body的background的写法

```HTML
<div style="background:url(/static/image/homebg.jpg)">
<body background="/static/image/homebg.jpg">
```

2. 更换头像的操作

更换涉及到文件的上传，我们得到文件的方式是通过html表单上传得到的这和改名字和改密码不一样，改名字和密码是直接修改数据库里面的文件，但是其实我们的图片和其他的文件都是在储存在固定的文件夹中的。我选择的方式是普通的用‘wb’的方式把图片文档写入我们的制定的static的photo文件夹，然后再更新我们的数据库信息（虽然文件是在数据库外面，但是我们调用图片是走数据库的）。虽然我们的网站不大，但是我们也得考虑删除原来的头像，在更新数据库之前我们还得先获取原来头像的信息，之后使用os.remove(path)把这个文件删除，代码如下

```python
avatar = request.FILES.get('new_avatar')
        name = avatar.name
        totalname = settings.MEDIA_ROOT+'/photo/'+name;
        with open(totalname, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        pro = Profile.objects.filter(idnumber=request.user.profile.idnumber)
        for p in pro:
            origin = p.avatar.name
        pro.update(avatar=totalname)
        os.remove(origin)
```

本博客的重中之重是写博文，得好使用，不复杂，我们就选择了处理本来就类html文档的md文档来生成网页，这其中涉及到处理一个代码高亮。我们使用了python的markdown库进行处理，基本的思路就是转化为html代码之后我们把这部分代码结合article.html的开头（你会看见我在views.py中最开始一大段的字符串都是写在新的html文档里面的），代码如下：

```python
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
            newhtml = codecs.open(settings.BASE_DIR+r'/blog/templates/article%d.html'%(total+1),'w',encoding='utf-8')
            newhtml.write(header)
            newhtml.write(html)
            newhtml.write(tail)
            newhtml.close()

```

### 用户管理

自带用户管理是Django的一大特点，你可以登陆127.0.0.1/admin用superuser的username和passowrd登陆进入管理页面，这个页面管理的东西都是你在admin.py中register的model以及默认的user（对，User是人register的，如果你想做一些炫酷的操作让User和之前我们定义的Profile和并在一起展示的话，你可以选择先把其解除register，这个部分留着以后改善的时候改善，不算难，方法也很多，也不是坑点）

但注意你在这个上面实现的文件的改动有一个问题，不会去删除已经上传的文件（我们之前的更换头像的删除是我们自己写的）可能需要管理员自己去删，后面我的改动会把用户，文章，评论三者写按找model的模型之间的关系重写的。

## 写法中的一些小手段

### 仅选择某个model的某些数据

比如我们只需要特定条件下User的姓名和id，你为了不返回给实际页面一个大的QuerySet，你可以单独把这两列选出来，转化为list（使用list()），然后使用zip函数，可以把两个相同长度的列表相同位序的元素组成一个元组，然后放在一个新的list中，你可以直接返回这个新的列表，还有元祖的顺序遍历是用x.0，x为元组，这是在python表单里面的写法，我怀疑对于list的非iterator遍历也是list.1这样的写法。

### 处理同一个html文件中的多个form

这个问题的产生主要是我的blog.html页面同时拥有搜索页面和提交新的的form，我如何去区分他们的呢，这个地方选择的是我去使用has_key("xxx")这个函数，你需要给两个表单的special input 元素写一个name（当然也是必须写的），然后你可以判定这次提交上来的表单里面是不是具有这个name，来判定是哪一个form，代码如下：

```python
if request.POST.has_key('search'):
  pass
elif request.POST.has_key("title"):
  pass
```

### 处理分页的问题

我们的文可能有很多条，我们如果用一个界面来展示所有的部分，这样会很不好看，也不友好，为此我使用了本身的Django的分页系统，并且结合了bootstrap的样式来实现了分页，具体代码如下：

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#我的代码都是复制原文档的，缩进可能略有问题，但不存在读不出层次结构，见谅
posts = Article.objects.all()#获得所有文章对象
posts = list(posts)#转化为list
        paginator = Paginator(posts, 3)#生成一个Paginator用来的分的是posts这个列表，每页3个
        page = request.GET.get('page')#前端在翻页的时候会返回一个page的页数
        try:
            posts = paginator.page(page)#获得定位该页的信息
            topics = Article.objects.all()[(int(page)-1)*3:int(page)*3]#获得具体这一页的文章
            ta =[]
            for post in topics:
                str = post.tags.split(" ")
                ta.append(str)
            topics = zip(topics,ta)
            links = Article.objects.all()[:5]
        except PageNotAnInteger:#下面是处理一些文章比较少的情况
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
```

我觉得整个东西的逻辑也不是很难，简单的一个切片，但是用Django的原生Paginator比较方便。

### 搜索功能和标签功能

搜索功能现在的开发水平还很低，我只用了最简单的字符串匹配，我后期可能会使用正则进行匹配，但似乎这样的效率还是很低，可能会选择使用python现有的搜索引擎的植入，在中文分词方面使用jieba

标签功能其实比较简单，简单的添加一个charField，tags之间用空格分开，使用的时候用split()函数把他们分开，点击标签可以进行搜索，这个方面后期也可以考虑下使用model关系之间联系一下各个部分

## 结语

我保证我传到github上面的代码一定可用，我只是具体的点到了各个部分，具体的语法要不就参照原代码，或者你们参照我给的链接的语法，以上。

​                                                                                                                                        2017年11月1日

​                                                                                                                                                  谭骁