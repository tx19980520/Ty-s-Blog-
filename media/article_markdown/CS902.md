# CS902

## 9.21

按位与：都为一则为一

按位或：两位有1则为1

按位异：两位不同为1

按位左移 << :*2

按位又移 >> :/2

负数存储：用2的补码，反过来加1

## 10.12

注意下python和cpp对于索引，切片都是左闭右开range也是最后一个不索引主义范围，相当于直接是小于符号

注意python关于函数的操作，字典和列表等高级数据结构（可删减项）不是拷贝一次进入函数，而是直接进入传指针进去，但是string 数字等类型在python中认为是常量，定义了就无法删（加可以的），这样就得注意我们别像原来cpp一样的简单的传进去数组，以为不会改变。

bool运算符的优先级 not > and > or

raw_input 只会把接收到的东西弄成字符串，input则是对应有类型。但都很好转型，只要能够用int()

chr()(Ascii to char) ord()(char to Ascii)

可以用"\"将两行连接

1. python函数定义中有这么两个特点


```python
def funcC(a, b=0):
  print a
  print b
```

b=0的意思是如果不传参数进来，函数默认此项为0

```python
def funcD(a,b,*c):
  print a
  print b
  print len(c)
  print c
funcD(1,2,3,4,5)
```

c 为(3,4,5)作为一个元组的形式出现

```python
def funcE(a,b,**c):
  print a
  print b
  for x in c:
    print x+':'+str(c[x])
funcE(1,2,name="Ty",age ="19")
```

上述的函数中**c是当作一个dictionary来处理的，我们则可以用key-value的方式来检索，dictionary的实际实现是用hash表来实现的，整体来讲类似于STL map （不是multi-map，因为不能有重复的键值）

python函数参数传递

1. 按位置来

2. 按key-value模式

   ​

变量的作用域：

跟cpp不一样的是python的作用域直接阐述是如下的

- python能够改变变量作用域的代码段是def、class、lambda.
- if/elif/else、try/except/finally、for/while 并不能涉及变量作用域的更改，也就是说他们的代码块中的变量，在外部也是可以访问的
- 变量搜索路径是：本地变量->全局变量

这里要强调的是第二条，我们在cpp里面退出循环，else等等的，在其中声明的变量全部消亡。

妈妈再也不用担心我声明变量在哪里了

函数若需引用并修改外部变量,可声明全局变量

```python
x= 10
def f():
  global x
  x += 10
  print x
print x
```

如果在local没有找到，在外层找，最后built-in里面去找

新式类和旧式类的问题

2.x中我们不显式的写继承于object都是旧式类，3.x中都默认为新式类

新式类继承是广度优先，旧式类是深度优先

```python
#作者：刘康
#链接：https://www.zhihu.com/question/22475395/answer/133787573
#来源：知乎
#著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

class A():
    def __init__(self):
        pass
    def save(self):
        print "This is from A"
class B(A):
    def __init__(self):
        pass
class C(A):
    def __init__(self):
        pass
    def save(self):
        print  "This is from C"
class D(B,C):
    def __init__(self):
        pass
fun =  D()
fun.save()

#经典类的答案： This is from A
#新式类的答案： This is from C
#发定义方式不同在Python 2.x 版本中，默认类都是旧式类，除非显式继承object。在Python 3.x 版本中，默认类就是新式类，无需显示继承object。在Python 2.x 中，定义旧式类的方式：class A:  # A是旧式类，因为没有显示继承object
    pass

class B(A):  # B是旧式类，因为B的基类A是旧式类
    pass 
```

 保持class与type的统一

对新式类的实例执行a.__class__与type(a)的结果是一致的，对于旧式类来说就不一样了。

了解一下\_\_init\_\_ ,\_\_new\_\_,\_\_call\_\__ 的区别

init是常见的初始化函数的，但是他在new被调用之后在运行的

一般情况我们不会自己写new，会调用父类的new，但必须知道其先于init

call的意义在于去掉函数和对象的相对概念，你定义的call的函数既可以使用对象名直接写函数，比如：

```python
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __call__(self, friend):
        print 'My name is %s...' % self.name
        print 'My friend is %s...' % friend
p = Person('Bob','male')
p('Tim')
#
My name is Bob...
My friend is Tim...
```

你可以直接把你的类当作函数来使用，但在使用之前你要对其进行实例化

在10-14通过实验得知

关于python私有变量

_使用于protected，\_\_使用与private

调用的时候都得是_类名\_\_函数名()

子类无法调用父类的private函数，这一点和cpp类似



python的奇怪报错

Recursion Error: maximum recursion depth exceeded

python 默认的递归层数只有900层左右，如果需要大规模的递归，可以用以下语法

```python
import sys
sys.setrecursionlimit(1000000)
```



如果不是写面对对象的问题，则我们在函数名前面加一个_是为了表示这是一个以文件为类的函数，仍然为protected，只能在本文档中使用。

## 10.15

如果你的类表现得像是一个列表，或者需要返回类中某重要列表的长度，则可以声明\_\_len\_\_函数，则你对外可以使用len(类的实例对象)来返回你想返回的值



python中try/except/else/finally体系的写法：

```python
try:
     Normal execution block#首先运行该区域，如果出现异常，交给python解释器进行操作，返回错误，进入except大板块
except A:#下述对于指定的错误有一些输出
     Exception A handle
except B:
     Exception B handle
except:#当然枚举不是好的想法，就把剩下不重要的错都放到了这里
     Other exception handle
else:#如果try中的语句完全没有问题，则执行else中的语句，当然你也可以不写
     if no exception,get here
finally:#不管出错还是没出错，有没有else finally中的语句是必须执行的
     print("finally")   
```

总结一下python当中asyncio的用法，相当于是创建事件循环，你向其中丢任务即可，对于多线程来讲，尤其是python的处理I\O密集型（HTTP，读写磁盘文件），现我能掌握的方式（非底层的写Threading），则是创建多个现成，向其中抛入在进程中定义的event-loop，我们在进程中产生任务，然后分配给各个线程处理，这比较符合python多线程的实际应用（我的爬虫创建了三个线程来处理获得网页源码，主进程在完成了分配任务之后开始进行对数据的写入文件）



python 标识符明明规则：

1.第一位可以是字母和下划线

2.后面是数字下划线字母都可以

3.**在3.x的Python中，标识符ASCII字母、下划线以及大多数非英文语言的字母，只要是Unicode编码的字母都可以充当引导字符，后续字符可以是任意引导符，或任意非空格字符，包括Unicode编码中认为是数字的任意字符。**

记住反正是不能有空格的



姑且总结一下最近接触的Django框架，python主流的网站框架

Django是MTV的开发模式，我们之前使用PHP写网站的时候，网站的建立都有一个基本的根目录的概念，我之前一直认为所有的软件开发都是这个样子，然后我发现我被打脸了，Django的基本理念是产生app，你访问某个地址，首先调用的是正则对应的函数，所有的地址都是这样，在urls.py中去寻找对应的函数，包括静态的资源。这一点要去适应（我还没适应），因为这样的设置会很多。Django对于面对对象的管理是非常不错的，都是在models.py进行编写的，在HTML当中的“嵌入”也基本上和PHP如出一辙 ，另外在debug和线下测试方面，省去了xampp这一大坨东西，不用去模拟整个状态，直接在cmd里面manage.py runserver 感觉到非常的舒适。

## 10.23

类中关于 \_\_str_\_的使用

这个函数主要是为print提供（或者一些特殊地方的类似print功能的调用和显示）的，你可以返回一些类中的信息。

```python
class user(object):
  def __init__(self,name,age):
    self.name = name
    self.age = age
  def __str__(self):
    return 'My name is '+self.name+", I'm "+self.age+'.'
a = user('Mike','15')
print a
#result My name is Mike, I'm 15.
```

# 10.26

首先面对对象的self不是必须的，只是第一位参数必须得是一个该类的对象，你只要自己知道就好了

其次\__repr__表示不调用print，你在交互模式当中写出一个对象的名字，它返回一个字符串并默认打印在屏幕上，如果你不重定义这个函数的话，将使用object的该函数，返回该对象的类型和地址等等额外的信息

对于python的运算符重载他不同于cpp的运算符重载，定义方式都是函数的方式，例如重载加法：

```python
class A(object):
  def __init__(self):
    pass
  def __add__(self,other):
    pass
  def __cmp__(self,other):
    pass
```

如果不知道是什么函数了就去文档里面查，以及，如果你想让加法有很多种情况，请自行使用一些方法比如```isinstance(a,b)```表示判断a,b是不是同一个类型，当然你可以直接索取其类型```type(a)``` 再去比较

\__dict__可以得到该对象的对应的类的所有函数方法，```hasattr()```判断是否有某个函数