## Django路由系统

一个用户向 Web 站点发送请求，是通过 URL 实现的，当 Web 服务器端接收到用户请求后，通过 MTV 的设计模式，我们可以得知，首先用户请求会到达相应的视图函数，那么视图函数又是怎样找到相应的访问资源的呢，在这里就用到了“路由系统”。

Django 中利用 **`ROOT_URLCONF`** 构建了 URL 与视图函数的映射关系。在 `django.conf.urls` 中封装了路由模块，新建的 Django 项目中提供了 urls.py（创建项目后自动生成的配置文件） 路由配置文件，urls.py 文件中定义了一个 urlpatterns 的列表，它是由 url( ) 实例对象组成的列表，Django 中 url 的定义就是在这个列表完成的。
```python
from django.conf.urls import url
urlpatterns=[
url(r '^admin/',admin.site.urls),
 ...
 ]
```
后台 Admin 管理系统的路由就定义在了列表第一个位置，下面我们对路由的语法格进行简单说明：

```python
url(regex,view,name=None)
```

上述 url 的参数解析如下：

- regex，匹配请求路径，用正则表达式表示；
- view，指定 regex 匹配路径所对应的视图函数的名称；
- name，是给 url 地址起个别名，在模板反向解析的时候使用，这个知识点后面还有介绍。

#### 1.  配置第一个URL实现页面访问

在 urls.py 的同级目录下，新建 views.py 文件，把它作为编写视图函数的 View 层，然后在 views.py 中编写如下代码：

```python
from django.http import HttpResponse
def page_view(request):    
    html='<h1>欢迎来到，C语言中文网，网址是http://c.biancheng.net</h>'    
    return HttpResponse(html)
```

假如现在有一个名叫 “myject”的 Django 项目，首先需要在 urls.py 文件中导入 views.py， 这么做的目的是把 URL 与视图层进行绑定，然后在 urls.py 的 urlpatterns 中编写如下代码：

```python
from django.conf.urls import url
from django.contrib import admin
from myject import views
urlpatterns = [    
    url(r'admin/', admin.site.urls),    
    (r'^page$/',views.page_view),]
```

上述代码解析：

- 代码的前 3 行分别对 URL 模块、admin 模块、以及视图层 views 做了导包操作；
- 路径地址被定义为 page，也就是在本机浏览器地址栏输入：http://127.0.0.1:8000/page 进行访问，`views.page_view`将 page/ 路径与对应的视图函数进行了关联。