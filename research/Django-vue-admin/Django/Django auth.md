## Django auth模块

### auth模块

Django 作为功能完善的 Web 框架充分考虑到这一点，它提供的 auth 模块能够快速的实现用户模块的基本功能。

新建项目后，Django 就把 auth 模块的所有功能提供给了开发者使用，开发者可以调用相应的接口，实现不同的功能需求。auth 模块定义了一张名叫 auth_user 的数据表，该表是 auth 模块的内建用户表，开发者调用 auth 模块的相应接口生成此表，auth_user 表的字段以及字段类型，如下所示。

```shell
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
| password     | varchar(128) | NO   |     | NULL    |                |
| last_login   | datetime(6)  | YES  |     | NULL    |                |
| is_superuser | tinyint(1)   | NO   |     | NULL    |                |
| username     | varchar(150) | NO   | UNI | NULL    |                |
| first_name   | varchar(30)  | NO   |     | NULL    |                |
| last_name    | varchar(150) | NO   |     | NULL    |                |
| email        | varchar(254) | NO   |     | NULL    |                |
| is_staff     | tinyint(1)   | NO   |     | NULL    |                |
| is_active    | tinyint(1)   | NO   |     | NULL    |                |
| date_joined  | datetime(6)  | NO   |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
11 rows in set (0.02 sec)#auth_user表
```

现在新建一张 auth_user 用户表，并为此表添加一个新用户 user。首先用如下方式引入 auth模块的 User 方法：

```python
from django.contrib.auth.models import User
```

然后通过下面方法创建新用户 user ，如下所示：

```python
user=User.objects.create_user(username='c语言中文网',password='123456',email='664104694@qq.com')save()#调用该方法保存数据 
```

同时也可以使用如下方法修改密码：

```python
user.set_password(password='12345abc')#会对原密码进行修改
```

根据具体的业务需求，还可以对表的字段进行增加、删除、更改。

当涉及到用户概念的时候也会产生用户权限问题，比如，如何划分普通用户和超级管理员用户？针对权限问题，Django 也提供了解决问题的方案，auth 模块提供了标准的权限管理系统，它配合 Admin 后台可以快速建立网站管理系统。

auth 模块提供了认证用户功能，可以用下面方式引入后使用：
```python
from django.contrib.auth import authenticate
```

然后使用关键字传参的方法来传递用户凭证，从而达到用户认证的目的：

```python
user = authenticate(username='c语言中文网',password='12345abc')
```
### auth模块的其他作用

auth 模块还实现一些其它的功能，比如：

- 用户的登录（login）、退出（logout）功能，封装在 `django.contrib.auth` 里；
- 用户权限系统封装在 `django.contrib.auth.models.Permission` 中 ，可以对用户的权限进行增加、修改、删除；
- 用户组可以通过 `from django.contrib.auth.models.Group` 导入后来创建组或者删除组。

### 实现用户的认证

authenticate 方法一般接受 username 与 password 作为参数，如果通过了认证，就返回认证的实例对象，否则就会返回 None

```python
In [1]: from django.contrib.auth import authenticate
In [2]: user=authenticate(username="bookstore",password="python_django")
In [3]: user
Out[3]: <User: bookstore>
In [4]: user=authenticate(username="bookstore",password="python")
In [5]: user is None
Out[5]: True
```

```python
def authenticate(request=None, **credentials):
    #__get_backends获取当前系统中定义的认证后端，并依次迭代
    for backend, backend_path in _get_backends(return_tuples=True):
        try:
            inspect.getcallargs(backend.authenticate, request, **credentials)
        except TypeError:
            #此后端不接受这些凭据作为参数。返回继续执行循环
            continue
        try:
             #通过当前的认证后端尝试获取 User，若获取不到就会抛出异常！
            user = backend.authenticate(request, **credentials)
        except PermissionDenied:
            #抛出异常Permission
            break
         #如果没有返回，继续执行下一个认证
        if user is None:
            continue
        #添加一个属性标志，代表后端认证成功
        user.backend = backend_path
        return user
    # 所提供的凭据对所有后端、触发信号无效
    user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)
    
def _get_backends(return_tuples=False):
    backends = []
    #AUTHENTICATION_BACKENDS 定义了当前系统可以用的身份认证列表
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        #加载后端
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    #如果未定义后端列表抛出异常
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends
```

### 校验用户登录状态@login_required

为了分析这个装饰器，我们还是首先看一下 Django 的源码，它的定义如下文件中：

`from django.contrib.auth.decorators import login_required`

#### 1) login_required函数参数说明

它的源码如下所示：

```python
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):    
    
    actual_decorator = user_passes_test(        
        lambda u: u.is_authenticated,        
        login_url=login_url,        
        redirect_field_name=redirect_field_name    
    )    
    if function:        
        return actual_decorator(function)    
    return actual_decorator
```

可以看出这个函数可以传递两个参数，这个函数做一下简单的分析：login_url 表示若为匿名用户访问时重定向的 URL，这里一般指定的都是登录页面的 URL 路径，默认的登录页需要在配置文件通过 LOGIN_URL 指定，然后通过使用以下方式进行调用 settings.py.LOGIN_URL；redirect_field_name 默认值为 next，作为 GET 的请求参数即参训字符串的形式，它的格式如下：

`127.0.0.1:8000/login/?next=/index/add_book/1`

这个参数用于登录后直接跳回到原先访问的视图。上述源码中可以看出该方法的实现核心是调用了 user_passes_test 方法。它需要传递三个参数，分析它的部分源码。如下所示：

```python
def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):    

	def decorator(view_func):        
        @wraps(view_func)        
        def _wrapped_view(request, *args, **kwargs):            #测试函数，通过后执行对应的视图函数            
            if test_func(request.user):                
                return view_func(request, *args, **kwargs)            
            path = request.build_absolute_uri()  #返回请求完成的URL             
            #获取登录页指定的URL            
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)            
            # If the login url is the same scheme and net location then just            
            # use the path as the "next" url.            
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]            
            current_scheme, current_netloc = urlparse(path)[:2]            
            #如果登录页的 URL与path的协议，域都相同则执行下面代码            
            if ((not login_scheme or login_scheme == current_scheme) and                    
                (not login_netloc or login_netloc == current_netloc)):                
                #获取视图的全路径，返回 HttpResponseRedirect                
                path = request.get_full_path()            
            
            from django.contrib.auth.views import redirect_to_login            
            return redirect_to_login(                
                path, resolved_login_url, redirect_field_name)        
        return _wrapped_view    
    return decorator
```

从 user_passes_test 的实现可以看出，它首先会判断 request.user.is_authenticated 是否会返回 True，如果成立，则会执行视图函数。否则，将重定向到登录页面。

#### 2) login_required应用方式

它的使用方式也非常的简单，只需要在视图函数加上方稍加改动即可，如下所示：

```python
from django.contrib.auth.decorators import login_required

@login_required
def search_title_views(request):    
    pass
```

如果在用户未登录的情况下访问这个视图的话，那么它将会跳转到登录页，需要注意的是由于这里没有指定 login_url，因此在配置文件中的 LOGIN_URL 要设置正确。

### 校验用户权限@permission_required

理解了如何校验登录状态的装饰器 @login_required， 下面我们对 @permission_required 进行讲解，这样大家理解起来会更加简单。我们还是看一下它的实现源码，如下所示：

```python
def permission_required(perm, login_url=None, raise_exception=False):    
    """   用于检查用户是否启用了特定权限的视图的装饰器，必要时可重定向到登录页。   
    如果给定了raise_exception参数，则会引发PermissionDenied异常。    
    """    
    def check_perms(user):         
        #如果指定权限是字符串，则将其放在元组中        
        if isinstance(perm, str):            
            perms = (perm,)        
        else:            
            perms = perm        
        #校验用户是否具有指定的权限        
        if user.has_perms(perms):            
            return True        
        # In case the 403 handler should be called raise the exception        
        if raise_exception:            
            raise PermissionDenied        
        #最终没有通过校验返回 False        
        return False    
    #check_perms 即为 user_passes_test中的测试函数    
    return user_passes_test(check_perms, login_url=login_url)
```

这个函数接受三个参数，它们的介绍如下：

- perm：需要校验的权限，可以是列表、元组、或者是字符串，如果是列表或者元组的话，那么用户同时拥有这些权限。

- login_url：没有指定权限的用户访问时会发生 302 重定向。

- raise_exception：默认为 False，如果设置为 True，则当没有权限的用户访问时将直接返回 403，由于权限的不足将禁止你的访问。

它的定义格式和 @login_required 是非常类似的。但是也有一点小小的区别，如下所示：

```python
@permission_required("index.can_view_book")#也可校验多个权限，在方法内添加即可
def book_add_views(request):    
    pass
```

我们可以这样理解，如果访问用户没有被授予 index.can_view_book 权限，就会跳转到登录页。这样不仅需要当前用户是已登录状态，还需要用户拥有 can_view_book 的权限。

### auth模块总结

auth 模块提供的主要功能总结如下：

- 实现并维护了用户与用户组的增加、删除、更改功能；
- 实现了用户权限与用户组权限的增加、删除、更改；
- 实现了可以自定义用户权限与用户组权限功能。

除了以上功能外，Django auth 模块还提供了权限验证等功能以及一些常用的方法。