## Django视图函数

### 1. 视图函数

在 Django 中，视图函数是一个 Python 函数或者类，开发者主要通过编写视图函数来实现业务逻辑。视图函数首先接受来自浏览器或者客户端的请求，并最终返回响应，视图函数返回的响应可以是 HTML 文件，也可以是 HTTP 协议中的 303 重定向。接下来编写一个简单的视图函数：

```python
from django.http import HttpResponse
def Hello_my_django(request):    
    return HttpResponse('<html><body>Hello my Django</body></html>')
```

下面针对以上 3 行代码做解析：

 1）HttpResponse视图响应类型

从 django.http 模块中导入 HttpResponse，从它简单的名字我们可以得知，它是一种视图的响应类型。

 2）视图函数参数request

我们定义了一个名为“Hello_my_django”的函数，Django 规定了，视图函数至少有一个参数，第一个参数必须是 request，request 是 HttpRequest 请求类型的对象，它携带了浏览器的请求信息，所以视图函数的第一个参数必须为 request。

 3）return视图响应

视图函数要返回响应内容，这里的响应内容是我们用 HTML 标签编写的，把它作为 HttpResponse 的对象返回给浏览器。

### 2. 视图函数执行过程

上面视图函数的代码虽然区区几行，但是已经充分体现了视图层的实现过程。 Django 收到请求以后，首先创建一个带有请求信息的 HttpRequset 对象，将 HttpRequest 的对象 request 作为第一个参数传递给视图函数，视图接收参数后继续向下执行，然后选择加载对应的视图，最后返回 HttpResponse 对象给浏览器。