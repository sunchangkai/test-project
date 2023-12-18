## install

gitee地址(主推)：https://gitee.com/liqianglog/django-vue-admin

github地址：https://github.com/liqianglog/django-vue-admin

### 1. install docker-compose

Linux 上我们可以从 Github 上下载它的二进制包来使用，最新发行的版本地址：https://github.com/docker/compose/releases。

运行以下命令以下载 Docker Compose 的当前稳定版本：

```shell
$ sudo curl -L "https://github.com/docker/compose/releases/download/v2.14.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

将可执行权限应用于二进制文件：

```shell
$ sudo chmod +x /usr/local/bin/docker-compose
```

创建软链：

```shell
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

测试是否安装成功：

```shell
$ docker-compose --version
docker-compose version 2.14.0, build 4667896b
```

### 2. 部署运行环境

使用docker-compose一键安装

#### 1. 自动构建，启动相关docker镜像

```shell
# 先安装docker-compose (自行百度安装),执行此命令等待安装，如有使用celery插件请打开docker-compose.yml中celery 部分注释
docker-compose up -d
```

#### 2. 更新backend/conf/env.py

主要更新数据库的相关配置

```shell
DATABASE_ENGINE = "django.db.backends.mysql"
DATABASE_NAME = 'django-vue-admin' # mysql 时使用

# 数据库地址 改为自己数据库地址
DATABASE_HOST = "10.38.49.30"
# # 数据库端口
DATABASE_PORT = 13306
# # 数据库用户名
DATABASE_USER = "root"
# # 数据库密码
DATABASE_PASSWORD = "123456"
```

#### 3. 初始化项目

```shell
# 初始化后端数据(第一次执行即可)
docker exec -ti dvadmin-django bash
python manage.py makemigrations 
python manage.py migrate
python manage.py init_area
python manage.py init
exit

前端地址：http://127.0.0.1:8080
后端地址：http://127.0.0.1:8080/api
# 在服务器上请把127.0.0.1 换成自己公网ip
账号：superadmin 密码：admin123456
```

#### 4. 常用docker-compose命令

````shell
# docker-compose stop
docker-compose down
#  docker-compose restart
docker-compose restart
#  docker-compose 启动时重新进行 build
docker-compose up -d --build
````

