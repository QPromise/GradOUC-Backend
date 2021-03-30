[TOC]

#  研在OUC小程序后端

# 【环境相关】

### 代码部署：

#### ps -ef | grep supervisor
#### ps -ef | grep 8000
#### systemctl restart nginx
#### supervisord -c ~/etc/supervisord.conf
#### supervisorctl -c ~/etc/supervisord.conf

### 静态文件收集：

* #### pipenv run python manage.py collectstatic

### 代码拉取：

* #### git pull https://gitee.com/qinchangshuai/GradOUC-Backend.git

### 环境相关：

* #### 来查看自身电脑的用户基础目录的路径python -m site --user-base

* #### 系统地址/usr/local/lib/python3.6/

* #### 查看用户组 groups qcs 属于qcs wheel

* #### 防火墙状态 systemctl status firewalld、开启service firewalld start、重启service firewalld restart、关闭service firewalld stop

* #### vim /etc/profile 添加环境变量  ` export PATH=$PATH:/home/qcs/.local/bin` 以及` export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/site-packages/`

### 端口相关：

* #### 访问本地端口 curl localhost:8000 

* #### 查看端口占用情况 netstat -tunlp | grep 8000

### 文件获取：

* #### 获取目标服务器文件 scp qcs@192.168.0.101:/home/kimi/test.txt

* #### 将本地文件放到目标服务器 scp * qcs@121.40.50.33:/home/qcs/


### 虚拟环境：

* #### 地址home/qcs/.local/share/virtualenvs/GradOUC-Backend-YFGLb5v1，开启source activate 

* 

  `pipenv --where`：寻找项目根目录；

  `pipenv install`：安装 `Pipfile` 中所列的所有包；

  `pipenv install --dev`：安装 `Pipfile` 中 `dev` 环境所列的所有包；

  `pipenv uninstall`：卸载所有包；

  `pipenv install pytest --dev`：在 `dev` 环境中安装 pytest 包；

  `pipenv lock`：确认 `Pipfile` 中所有包已安装，并根据安装版本生成 `Pipfile.lock`；

  `pipenv shell`：应用虚拟环境。

### 解决上传后台图片500错误

* #### https://blog.csdn.net/peng2hui1314/article/details/105572626

### 解决申请https lets错误

* #### https://github.com/certbot/certbot/issues/7645

### 域名加前缀，需要添加解析

* #### 到[云解析DNS](https://dns.console.aliyun.com/?spm=5176.100251.111252.24.76304f15NaN4Xi#/)/[域名解析](https://dns.console.aliyun.com/?spm=5176.100251.111252.24.76304f15NaN4Xi#/dns/domainList)/解析设置

### 如果出现500或502错误，需要查看nginx日志，在/var/log/nginx，nginx在cd /etc/nginx下

### Let's证书续费：

* #### 如果提示你Challenge failed for domain xxxx 使用下面这个去续费！
  certbot certonly -d leoqin.fun --preferred-challenges dns --manual --server https://acme-v02.api.letsencrypt.org/directory

* #### /var/log/letsencrypt

* #### /etc/letsencrypt/renewal/leoqin.fun.conf

* #### sudo certbot --nginx

### 数据迁移：

* #### 导出 JSON 格式的数据：python manage.py dumpdata > db.json；生成新的数据库表：python manage.py migrate；导入 JSON 数据：python manage.py loaddata db.json。

### 更换数据源

* #### pip3 install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade gevent --users



# 【项目部署】

### 创建一个超级用户

顺利连接到远程服务器了，如果是一台全新服务器的话，通常我们是以 root 用户登录的。在 root 下部署代码不够安全，最好是建一个新用户（如果你已经以非 root 用户登录的话可以跳过这一步）。下面的一些列命令将创建一个拥有超级权限的新用户（把 qcs 替换成你自己想要的用户名，我这里取我的名字拼音 qcs）：

```
# 在 root 用户下运行这条命令创建一个新用户，qcs 是用户名
# 我取的用户名是 qcs
# 选择一个你喜欢的用户名，不一定非得和我的相同
root@server:~# adduser qcs

# 为新用户设置密码
# 注意在输密码的时候不会有字符显示，不要以为键盘坏了，正常输入即可
root@server:~# passwd qcs

# 把新创建的用户加入超级权限组
root@server:~# usermod -aG wheel qcs

# 切换到创建的新用户
root@server:~# su - qcs

# 切换成功，@符号前面已经是新用户名而不是 root 了
qcs@server:$
```

新用户创建并切换成功了。如果是新服务器的话，最好先更新一下系统，避免因为版本太旧而给后面安装软件带来麻烦。运行下面的两条命令：

```
qcs@server:$ sudo yum update
qcs@server:$ sudo yum upgrade
```

## 更新 SQLite3

为了方便，我们博客使用了 SQLite3 数据库，django 2.2 要求 SQLite3 数据库版本在 3.8.3 以上，而 CentOS 7 系统自带版本低于 django 2.2 所要求的最低版本，所以首先来更新 SQLite3 的版本。

> **注意**
>
> 有可能你使用的服务器系统发行版 SQLite3 已经高于 3.8.3，这一步就可以跳过。如何查看 SQLite3 的版本呢？请执行 sqlite3 --version

首先登陆到 [sqlite 的官方下载地址](https://sqlite.org/download.html)，查看最新发布的版本，截止到本教程完成时，其最新版本为 3.29.0，找到该版本的源码压缩包，复制其下载链接，然后通过 wget 命令下载到服务器（我一般习惯将源码放在 ~/src 目录下。）

```
# 创建 src 目录并进到这个目录
qcs@server:$ mkdir -p ~/src
qcs@server:$ cd ~/src

# 下载 sqlite3 源码并解压安装
qcs@server:$ wget https://sqlite.org/2019/sqlite-autoconf-3290000.tar.gz
qcs@server:$ tar zxvf sqlite-autoconf-3290000.tar.gz
qcs@server:$ cd sqlite-autoconf-3290000
qcs@server:$ ./configure
qcs@server:$ make
qcs@server:$ sudo make install
```

> 小贴士：
>
> 如果 wget 命令不存在，使用 sudo yum install -y wget 安装即可。

至此 SQLite3 更新完毕，接下来安装 Python3。

## 安装 Python3 和 Pipenv

CentOS 7 自带的 Python 发行版为 2.7，因此需要安装 Python3，为了兼容性，我们安装 Python 3.6.4。

首先安装可能的依赖：

```
qcs@server:$ sudo yum install -y openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
```

然后下载 Python 3.6.4 的源码并解压：

```
qcs@server:$ cd ~/src
qcs@server:$ wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
qcs@server:$ tar -zxvf Python-3.6.4.tgz
```

最后编译安装：

```
qcs@server:$ cd Python-3.6.4
qcs@server:$ ./configure LD_RUN_PATH=/usr/local/lib LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include"
qcs@server:$ make LD_RUN_PATH=/usr/local/lib
qcs@server:$ sudo make install
```

注意这里安装 Python 时，Python 会依赖 SQLite3 的库，所以在 configure 时通过 LD_RUN_PATH 指定依赖的搜索目录（因为我们之前更新了 SQLite3 的版本，指定依赖搜索目录确保使用新的 SQLite3 依赖库），另外两个参数作用类似。

然后输入 python3.6 -V 和 pip3.6 -V 命令测试安装结果，输出版本号说明安装成功了。

有了 pip，就可以安装 Pipenv 了：

```
qcs@server:$ sudo pip3.6 install pipenv
```

> 小贴士：
>
> 如果以上命令报错，可能是因为 pip3.6 安装在当前用户的 bin 路径下（/usr/local/bin/），使用 **pip3.6 install pipenv --users** 命令也把 Pipenv 安装到当前用户的 bin 路径下就可以了，会安装到/home/qcs/.local/bin文件下

<u>**需要vim /etc/profile 添加环境变量  ` export PATH=$PATH:/home/qcs/.local/bin` 以及` export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/site-packages/`**</u>

## 部署代码

接下来开始准备部署代码，让我们的博客应用在服务上跑起来，这和在本地开发时的过程是一模一样的。不过为了将应用部署到服务器上，我们首先要对项目做一点配置，打开 settings.py，找到 `ALLOWED_HOSTS`，将其修改为：

```
PgOUC/settings.py

ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '.leoqin.fun']
```

指定了 `ALLOWED_HOSTS` 的值后，django 将只允许通过指定的域名访问我们的应用，比如这里只允许通过 127.0.0.1，localhost 以及 leoqin.fun 和其任意子域名（域名前加一个点表示允许访问该域名下的子域名）访问（即 HTTP 报文头部中 Host 的值必须是以上指定的域名，通常你在浏览器输入域名访问网站时，Host 的值就会被设置为网站的域名），这样可以避免 HTTP Host 头攻击。

django 项目中会有一些 CSS、JavaScript 等静态文件，为了能够方便地让 Nginx 处理这些静态文件的请求，我们把项目中的全部静态文件收集到一个统一的目录下，这个目录通常位于 django 项目的根目录，并且命名为 static。为了完成这些任务，需要在项目的配置文件里做一些必要的配置：



```
PgOUC/settings.py

# 其他配置...

STATIC_URL = '/static/'
# 加入下面的配置
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```


`STATIC_ROOT` 即指定静态文件的收集路径，这里指定为 BASE_DIR（项目根目录，在 settings.py 文件起始处定义）下的 static 文件夹。



现在的关键是把代码传到服务器上来了，这里我们使用 git。首先安装 git：

```
qcs@server:$ sudo  yum install -y git
```

将代码上传到 GitHub 等代码托管平台，这样我们就可以方便地把代码拉取到服务器了。Git 和 GitHub 的使用相信你已经很熟悉了，这里就不赘述过程。如果不知道如何使用地话可以自行百度相关教程。**注意数据库文件不要上传！**

我通常喜欢把应用代码放在 ~/apps/ 目录下，先来设置一下服务器的文件结构，用于存放应用代码等相关文件：

```
# 在用户目录下创建 apps 目录并进入
qcs@server:$ mkdir -p ~/apps
qcs@server:$ cd ~/apps

# 拉取博客代码
qcs@server:$ git clone https://gitee.com/qinchangshuai/GradOUC-Backend.git
```

然后进入到项目根目录，安装项目依赖：

```
qcs@server:$ cd ~/apps/GradOUC-Backend

qcs@server:$ pipenv install --deploy --ignore-pipfile
```

<u>**这里会失败，只要添加python的环境变量就行，虚拟环境用**</u>

```
/home/qcs/.local/share/virtualenvs/GradOUC-Backend-YFGLb5v1
```

<u>**所需要的包在这我们添加的环境变量下面**</u>

```
/usr/local/lib/python3.6/site-packages/
```

**<u>使用` pip3.6 install xxxx包`来进行安装。</u>**

这里指定 `--deploy` 参数，Pipenv 将只会安装 Pipfile 中 [packages] 下指定的依赖。因为我们现在是在线上环境进行部署，仅用于开发环境的相关依赖我们并不需要。

`--ignore-pipfile` 将会使 Pipenv 从 Pipfile.lock 文件中安装项目依赖。Pipfile.lock 记录了项目依赖的精确信息，从这里读取依赖信息能够确保依赖信息被无意中修改或者破坏而使得运行环境因为依赖包的缘故出现不可预料的问题。

Pipenv 会自动帮我们创建虚拟环境，然后将项目依赖安装到虚拟环境下。

然后创建一下数据库：

```
qcs@server:$ pipenv run python manage.py migrate
```

启动开发服务器：

```
qcs@server:$ pipenv run python manage.py runserver 0.0.0.0:8000
```

这里我们启动开发服务器时指定了服务器运行的 ip 和端口，这将允许通过公网 ip 的 8000 端口访问我们的博客。

访问 ip:8000，可以看到访问成功（其中 ip 为你服务器的公网 ip）。

## 使用 Gunicorn

django 官方文档强调使用 runserver 开启的开发服务器仅用于开发测试，不建议用于生产环境。所以我们使用流行的 Gunicorn 来启动可以用于线上环境的服务器。

首先进入到项目根目录，安装 Gunicorn：

```
qcs@server:$ pipenv install gunicorn
```

由于我们在服务端修改安装了 gunicorn，代码中 Pipfile 文件和 Pipfile.lock 文件会被更新，因此别忘了把改动同步到本地，具体做法可以自行学习，以下是一个参考：

```
# 服务端提交代码
qcs@server:$ git add Pipfile Pipfile.lock
qcs@server:$ git commit -m "add gunicorn dependency"
qcs@server:$ git push

# 本地拉取代码
git pull
```

回到线上服务器，在项目根目录，执行下面的命令启动服务：

```
qcs@server:$ pipenv run gunicorn PgOUC.wsgi -w 2 -k gthread -b 0.0.0.0:8000
```

来解释一下各个参数的含义。

`-w 2 表示启动 2 个 worker 用于处理请求（一个 worker 可以理解为一个进程），通常将 worker 数目设置为 CPU 核心数的 2-4 倍。

`-k gthread` 指定每个 worker 处理请求的方式，根据大家的实践，指定为 `gthread` 的异步模式能获取比较高的性能，因此我们采用这种模式。

`-b 0.0.0.0:8000`，将服务绑定到 8000 端口，运行通过公网 ip 和 8000 端口访问应用。

访问 ip:8000（ip 为你服务器的公网 ip），应用成功访问了，但是我们看到样式完全乱了。别急，这不是 bug！此前我们使用 django 自带的开发服务器，它会自动帮我们处理静态样式文件，但是 Gunicorn 并不会帮我们这么做。因为处理静态文件并不是 Gunicorn 所擅长的事，应该将它交给更加专业的服务应用来做，比如 Nginx。

## 启动 Nginx 服务器

Nginx (engine x) 是一个高性能的 HTTP 和反向代理 web 服务器，它的功能非常多，这里我们主要用它来处理静态文件以及将非静态文件的请求反向代理给 Gunicorn。

当我们访问一个博客文章详情页面时，服务器会接收到下面两种请求：

- 显示文章的详情信息，这些信息通常保存在数据库里，因此需要调用数据库获取数据。
- 图片、css、js 等存在服务器某个文件夹下的静态文件。

对于前一种请求，博客文章的数据需要借助 django 从数据库中获取，Nginx 处理不了，它就会把这个请求转发给 运行在 Gunicorn 服务中的 django 应用，让 django 去处理。而对于后一种静态文件的请求，只需要去这些静态文件所在的文件夹获取，Nginx 就会代为处理，不再麻烦 django。

用 django 去获取静态文件是很耗时的，但 Nginx 可以很高效地处理，这就是我们要使用 Nginx 的原因。

首先安装 Nginx：

```
qcs@server:$ sudo yum install epel-release -y
qcs@server:$ sudo yum install nginx -y
```

运行下面的命令启动 Nginx 服务：

```
qcs@server:$ sudo systemctl start nginx
```

在浏览器输入 ip（不输入端口则默认为 80 端口，Nginx 默认在 80 端口监听请求），看到 Nginx 的欢迎界面说明 Nginx 启动成功了。

## 配置 Nginx

Nginx 的配置位于 /etc/nginx/nginx.conf 文件中，你可以打开这个文件看看里面的内容，下面是一些关键性的配置：

```
user nobody nobody;
...
http {
    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        }
    }
}
```

首先是这个 user 配置，用于指定 Nginx 进程运行时的用户和组（分别为第一个和第二个参数），为了防止可能的权限问题，我们改成当前系统用户（我的用户名是 qcs，所属组 qcs，记得改成你自己服务器中运行的用户和组，修改完后记得保存文件内容）：

```
user qcs;
```

然后在 http 配置下有一个 server 模块，server 模块用于配置一个虚拟服务，使这个虚拟服务监听指定的端口和域名。你可以配置多个 server，这样就会启动多个虚拟服务，用于监听不同端口，或者是同一个端口，但是不同的域名，这样你就可以在同一服务器部署多个 web 应用了。

这个 server 的配置我们下面会详细讲解，再来看看 server 下的 include，include 会将指定路径中配置文件包含进来，这样便于配置的模块化管理，例如我们可以把不同 web 应用的配置放到 /etc/nginx/conf.d/ 目录下，这样 nginx 会把这个目录下所有以 .conf 结尾的文件内容包含到 nginx.conf 的配置中来，而无需把所有配置都堆到 nginx.conf 中，使得配置文件十分臃肿。

我们来配置博客应用，上面说了，为了模块化管理，我们将配置写到 /etc/nginx/conf.d/ 目录下。先在服务器的 conf.d 目录下新建一个配置文件，我把它叫做 GradOUC-Backend.conf。写入下面的配置内容：

```
server {
    charset utf-8;
    listen 80;
    server_name gradouc-backend.leoqin.fun;

    location /static {
        alias /home/qcs/apps/GradOUC-Backend/static;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

首先我们配置了一个虚拟服务，编码方式为 utf-8，监听于 80 端口。

服务的域名为 gradouc-backend.leoqin.fun，所以来自这个域名的请求都会被这个服务所处理。

所有URL 匹配 /static 的请求均由 Nginx 处理，alias 指明了静态文件的存放目录，这样 Nginx 就可以在这个目录下找到请求的文件返回给客户端。

其它请求转发给运行在本机 8000 端口的应用程序处理，我们会在这个端口启动 Gunicorn 用于处理 Nginx 转发过来的请求。

重启 nginx 使得配置生效：

```
qcs@server:$ sudo systemctl restart nginx
```

## 关闭 DEBUG 模式，收集静态文件

开发环境下，django 为了调试方便，会将 settings.py 文件中的 DEBUG 选项配置为 True，这样如果程序运行出错，调试信息将一览无余，这在开发时很方便，但部署到线上就会带来巨大安全隐患，所以我们把 DEBUG 选项设置为 False，关闭调试模式，在本地将 settings.py 中的 DEBUG 为：

```
DEBUG=False
```

**线上服务器更新最新的代码**，然后运行命令收集静态文件到之前配置的 STATIC_ROOT 目录下：

```
qcs@server:$ pipenv run python manage.py collectstatic
```

然后使用 Gunicorn 启动服务。

```
qcs@server:$ pipenv run gunicorn PgOUC.wsgi -w 2 -k gthread -b 127.0.0.1:8000
```

现在，访问配置的域名 hellodjango-blog-tutorial-demo.leoqin.fun（改成你自己在 Nginx 中配置的域名），可以看到博客成功部署！

## 管理 Gunicorn 进程

现在 Gunicorn 是我们手工启动的，一旦我们退出 shell，服务器就关闭了，博客无法访问。就算在后台启动 Gunicorn，万一哪天服务器崩溃重启了又得重新登录服务器去启动，非常麻烦。为此使用 Supervisor 来管理 Gunicorn 进程，这样当服务器重新启动或者 Gunicorn 进程意外崩溃后，Supervisor 会帮我们自动重启 Gunicorn。

先按 Ctrl + C 停止刚才启动的 Gunicorn 服务进程。

首先安装 Supervisor。注意这里使用的是**系统自带的 pip2**，因为截至本教程书写时 Supervisor 还不支持 Python3，不过这并不影响使用。

```
qcs@server:$ pip install supervisor
```

为了方便，我一般会设置如下的目录结构（位于 ~/etc 目录下）来管理 Supervisor 有关的文件：

```
~/etc

├── supervisor
│   ├── conf.d
│   └── var
│       ├── log
└── supervisord.conf
```

其中 supervisord.conf 是 Supervior 的配置文件，它会包含 conf.d 下的配置。var 目录下用于存放一些经常变动的文件，例如 socket 文件，pid 文件，log 下则存放日志文件。

首先来建立上述的目录结构：

```
qcs@server:$ mkdir -p ~/etc/supervisor/conf.d
qcs@server:$ mkdir -p ~/etc/supervisor/var/log
```

然后进入 ~/etc 目录下生成 Supervisor 的配置文件：

```
qcs@server:$ cd ~/etc
qcs@server:$ echo_supervisord_conf > supervisord.conf
```

修改 supervisor.conf，让 Supervisor 进程产生的一些文件生成到上面我们创建的目录下，而不是其默认指定的地方。

首先找到 [unix_http_server] 版块，将 file 设置改为如下的值：

```
[unix_http_server]
file=/home/qcs/etc/supervisor/var/supervisor.sock
```

即让 socket 文件生成在 ~/etc/supervisor/var/ 目录下。注意 supervisor 不支持将 ~ 展开为用户 home 目录，所以要用绝对路径指定。

类似的修改 [supervisord] 板块下的 logfile 和 pidfile 文件的路径，还有 user 改为系统用户，这样 supervisor 启动的进程将以系统用户运行，避免可能的权限问题：

```
logfile=/home/qcs/etc/supervisor/var/log/supervisord.log
pidfile=/home/qcs/etc/supervisor/var/supervisord.pid
user=qcs
```

还有 [supervisorctl] 板块下：

```
serverurl=unix:///home/qcs/etc/supervisor/var/supervisor.sock
```

[include] 版块，将 /home/qcs/etc/supervisor/conf.d/ 目录下所有以 .ini 结尾的文件内容包含到配置中来，这样便于配置的模块化管理，和之前 Nginx 配置文件的处理方式是类似的。

```
files = /home/qcs/etc/supervisor/conf.d/*.ini
```

然后我们到 conf.d 新建我们博客应用的配置：

```
[program:gradouc-backend]
command=pipenv run gunicorn PgOUC.wsgi -w 2 -k gthread -b 127.0.0.1:8000
directory=/home/qcs/apps/GradOUC-Backend
autostart=true
autorestart=unexpected
user=qcs
stdout_logfile=/home/qcs/etc/supervisor/var/log/gradouc-backend-stdout.log
stderr_logfile=/home/qcs/etc/supervisor/var/log/gradouc-backend-stderr.log
```

说一下各项配置的含义：

[program:gradouc-backend] 指明运行应用的进程，名为 gradouc-backend。

command 为进程启动时执行的命令。

directory 指定执行命令时所在的目录。

autostart 随 Supervisor 启动自动启动进程。

autorestart 进程意外退出时重启。

user 进程运行的用户，防止权限问题。

stdout_logfile，stderr_logfile 日志输出文件。

启动 Supervisor

```
qcs@server:$ supervisord -c ~/etc/supervisord.conf
```

-c 指定 Supervisr 启动时的配置文件。

进入 supervisorctl 进程管理控制台：

```
qcs@server:$ supervisorctl -c ~/etc/supervisord.conf
```

执行 update 命令更新配置文件并启动应用。

浏览器输入域名，可以看到服务已经正常启动了。

## 申请Let's Encrypt

首先安装 Let’s Encrypt 提供的证书申请工具。登录 https://certbot.eff.org/，选择我们博客网站使用的服务器软件和操作系统。教程中以 Nginx 和 CentOS 7 为例：

首先安装必要工具：

```
$ sudo yum -y install yum-utils
$ sudo sudo yum install -y certbot python2-certbot-nginx
```

certbot python2-certbot-nginx 是 Let’s Encrypt 提供的 HTTPS 证书申请的工具，python2-certbot-nginx 是专门针对 Nginx 的插件，使得 Nginx 运行的服务申请证书更加简单方便。

然后运行证书申请命令：

```
$ sudo certbot --nginx
```

> 注意
>
> 经测试，运行上述命令后有可能报 ImportError: No module named 'requests.packages.urllib3' 的错误，这是由于 requests 和 urlib3 版本过低所致（可以参考这个 [issue](https://github.com/certbot/certbot/issues/5104) 的讨论），解决办法是重装它们，运行下面的命令：
>
> ```
> pip uninstall requests
> pip uninstall urllib3
> yum remove python-urllib3
> yum remove python-requests
> 如果上面的不行，用下面这个
> sudo pip uninstall requests
> sudo pip uninstall urllib3
> sudo yum remove python-urllib3
> sudo yum remove python-requests
> sudo yum install python-urllib3
> sudo yum install python-requests
> ```
>
> 然后重新安装 certbot，由于它依赖上面两个包，所以重装时会一并装上：
>
> ```
> bash $ sudo yum install -y certbot python2-certbot-nginx
> ```

重新执行证书申请命令：sudo certbot --nginx

会有一系列交互式的提示，首先会让你输入邮箱，用于订阅。然后输入 a 同意他们的政策。

接着 certbot 会自动扫描出来域名，根据提示输入想开启 HTTPS 的域名标号：

> Which names would you like to activate HTTPS for?
>
> ------
>
> 1: gradouc-backend.leoqin.fun
>
> ------
>
> Select the appropriate numbers separated by commas and/or spaces, or leave input
> blank to select all options shown (Enter 'c' to cancel): 1

然后 certbot 会做一个域名校验，证明你对这个域名有控制权限。验证通过后，Let's Encrypt 就会把证书颁发给你。

最后会提示你是否把 HTTP 重定向到 HTTPS，当然选择是，这样 certbot 会自动帮我们修改 Nginx 的配置，将 HTTP 重定向到 HTTPS，如果用户使用 HTTP 协议访问我们的博客网站，就会重定向到 HTTPS 协议访问，确保安全性。

> Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
>
> ------
>
> 1: No redirect - Make no further changes to the webserver configuration.
> 2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
> new sites, or if you're confident your site works on HTTPS. You can undo this
> change by editing your web server's configuration.
>
> ------
>
> Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 2
> Redirecting all traffic on port 80 to ssl in /etc/nginx/conf.d/django-blog-tutorial-v2.conf

certbot 申请的证书只有 3 个月有效期，不过没有关系，certbot 可以无限续期，我们增加一条 crontab 定时任务用来执行 certbot 自动续期任务，这样一次申请，终生使用。

打开 /etc/crontab，增加定时任务：

```
echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew" | sudo tee -a /etc/crontab > /dev/null
```

这里配置每天 12 点执行自动续期命令。