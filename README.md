官方文档：[http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#where-to-go-from-here](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#where-to-go-from-here)
官方配置参数：[http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration](http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration)

## 安装Python3
```
$ wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
$ tar zxvf Python-3.7.6.tgz
$ cd Python-3.7.6.tgz
$ ./configure --enable-optimizations --prefix=/usr/local/python3.7
$ make&&make install
```

## 使用docker安装RabbitMQ
```
$ docker pull rabbitmq
$ docker run -d --name MyRabbitMQ -p 5672:5672 rabbitmq
```
## 创建Python3虚拟环境
```
$ /usr/local/python3.7/easy_install virtualenv
$ mkdir {本地目录存储}/virtualenvs/
$ cd {本地目录存储}/virtualenvs/
$ virtualenv py37
Installing setuptools, pip, wheel...done
# 后续pip安装使用/{本地目录存储}/virtualenvs/py37/bin/pip来安装
$ pip install Django
$ pip install celery
$ {虚拟环境目录}/django-admin startproject celery_demo
```

### 创建Django工程
```
$ {虚拟环境目录}/django-admin startproject celery_demo
```
创建后的Django目录：
```
- celery_demo/
  - manage.py
  - celery_demo/
    - __init__.py
    - settings.py
    - urls.py
```
创建celery.py用于定义Celery实例

```
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_demo.settings')
app = Celery('celery_demo')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery4版本以前需要配置settings.CELERY_IMPORTS来导入目录中的tasks.py, 通过autodiscover_tasks会自动发现这些tasks
app.autodiscover_tasks()
```
在最外层目录创建__init__.py文件中
```
- celery_demo/
 # 添加_init_.py文件
  - __init__.py
  - manage.py
  - celery_demo/
    - __init__.py
    - settings.py
    - urls.py
```
编辑代码:
```
#  该行导入到放在最顶部
from __future__ import absolute_import, unicode_literals

# 这样可以确保在Django启动时加载应用
from .celery import app as celery_app

__all__ = ('celery_app',)
```

新建app并创建tasks.py
```
$ django-admin startapp user
```
创建后目录变化为:
```
- celery_demo/
 # 添加_init_.py文件
  - __init__.py
  - manage.py
  - celery_demo/
    - __init__.py
    - settings.py
    - urls.py
- user/
    - __init__.py
    - views.py
    - urls.py
```
在user目录中创建tasks.py（tasks文件不要和celery实例文件放在相同目录下，否则启动celery worker会报错Received unregistered task of type 'xxx.tasks.test_celery'.）

*编辑代码:*
```
import time

from celery_demo.celery import app


@app.task()
def test_celery():
    time.sleep(10)
    return "Run test_celery ok"

```

## 启动Celery Worker
注意执行目录要在celery.py的外层目录，否则会报错The module celery_demo.celery was not found.， -l info表示输出调试信息
```
$ {虚拟环境目录}/celery -A celery_demo worker -l info
Please specify a different user using the --uid option.

User information: uid=0 euid=0 gid=0 egid=0

  uid=uid, euid=euid, gid=gid, egid=egid,

 -------------- celery@myMacBook-Pro.local v4.4.0 (cliffs)
--- ***** -----
-- ******* ---- Darwin-19.3.0-x86_64-i386-64bit 2020-02-18 18:46:28
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         celery_demo:0x102b99e50
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:     disabled://
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . user.tasks.test_celery
```
## 全部配置完成，测试任务进入Django shell
```
$ {虚拟环境目录}/python manage.py runserver
> from user import tasks
> result = tasks.test_celery.delay()
<AsyncResult: 2fe3d898-6598-4701-b665-ecd6fef4198d>
```
delay()返回的结果实例：
```result.state```：表示当前任务的执行状态，变化由```PENDING-> STARTED-> SUCCESS```，如果任务执行出现异常，状态变为```FAILUTE```
```result.id```：当前任务的```taskid```可以通过id获取当前任务的状态
```
> from proj.celery import app
> res = app.AsyncResult('taskid')
> res.state
SUCCESS
```

### 后台运行Celery
```
$ celery multi start  -A celery_demo -l info
```

### 重启Celery
```
$ celery multi restart  -A celery_demo -l info
```
