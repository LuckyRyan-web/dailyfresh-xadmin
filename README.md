## 项目说明

 本项目是基于B2C的商业模式的设计思路的天天生鲜商城，以其完整的功能，为用户提供一个完整的购物支付环境

**项目截图：**

![1568988886523](C:\Users\LY\Pictures\博客照片\截图1.png)



![1568988929485](C:\Users\LY\Pictures\博客照片\截图2.png)

![1568989129928](C:\Users\LY\Pictures\博客照片\截图3.png)

![1568989167308](C:\Users\LY\Pictures\博客照片\截图4.png)

![1568989391782](C:\Users\LY\Pictures\博客照片\截图5.png)

## 项目架构

​	这个项目我使用了两个数据库来部署，使用数据库A去部署Django网站和Celery异步操作，服务器B来使用FDFS静态资源存储和用来确认使用的是缓存还是数据库查询的Nginx端口转发

​	在本地运行的话建议使用虚拟机或者阿里云的学生服务器来运行，阿里云服务器记得开启端口

## 技术栈

1. 基于Python3.6和Django1.9技术设计
2. 数据库：redis、mysql
3. 任务队列：celery框架
4. 静态资源存储：FastDFS
5. 商品搜索：基于haystack来使用whoosh
6. Web服务器：Nginx+uwsgi



## 本地运行项目

1. 建议创建一个虚拟环境来运行
   python manage.py startapp dailyfresh
   然后一键安装依赖包
   pip install -r requirements.txt
2. 在setting.py中配置自己的服务器或者虚拟机的ip和端口
3. 在celery_tasks配置自己的服务器或者虚拟机的redis端口，然后使用`celery -A celery_tasks.tasks worker -l info -P eventlet ` 启动celery服务
4. 在使用redis缓存记录的时候看看自己的redis数据库有没有值先，redis-cli -h 127.0.0.1 -p 6379，Flushdb(删除单个数据库的所有键值对)
5. 在自己部署的服务器上，使用[文档](https://blog.csdn.net/busishenren/article/details/83584885)里面的步骤去部署，记得[开放端口](https://www.cnblogs.com/heqiuyong/p/10460150.html)
6. 改写utils.fdfs里面的client.conf的base_path和tracker_server字段



## 在服务器上运行项目

在setting.py中，修改这两个字段为

```
DEBUG=FALSE
ALLOWED_HOSTS=[‘*’] 
```



## 开发中参考到的博客

[xadmin使用大全](https://segmentfault.com/a/1190000016082270?utm_source=tag-newest)

[富文本编辑器的使用1](https://www.cnblogs.com/zmdComeOn/p/11345418.html)

[富文本编辑器的使用2](https://github.com/zhangfisher/DjangoUeditor)

[xadmin集成UEditor](https://blog.csdn.net/wgpython/article/details/79585205)

[阿里云centos服务器安装python3.6](https://www.cnblogs.com/charles8866/p/8366695.html)

[阿里云centos安装pip3](https://www.centos.bz/2018/03/centos-7%E5%AE%89%E8%A3%85pip3/)

[celery在win10系统运行的问题1](https://www.cnblogs.com/springionic/p/10959353.html)

[celery在win10系统运行的问题2](https://blog.csdn.net/qq_30242609/article/details/79047660)

[django-redis使用文档](https://django-redis-chs.readthedocs.io/zh_CN/latest/)

[阿里云centos7服务器安装Nginx](https://blog.csdn.net/qq_32953079/article/details/81975160)

```
补充一下

开启Nginx命令: ./nginx -s stop

刷新Nginx命令: ./nginx -s reload
```

[阿里云Centos7一步一步搭建FastDFS和部署Nginx](https://blog.csdn.net/busishenren/article/details/83584885)

[阿里云centos7开启端口](https://www.cnblogs.com/heqiuyong/p/10460150.html)

[xadmin使用admin的save_model功能](https://blog.csdn.net/qq_35531549/article/details/86609258)

[xadmin与admin对比](https://www.jianshu.com/p/05edc51368fd)

这里切记，阿里云服务器要先开外面的防火墙规则，然后再去开启内部的端口，然后再重启防火墙才有效

这里切记切记，不要先安装python3在安装fdfs，如果安装了开启防火墙会出问题，也不能使用fdfs通过端口访问，如果已经安装了python3，那么看这里[安装Python3之后防火墙无法启动](https://blog.csdn.net/cenylon/article/details/79954524)



## 性能优化

1. 将admin改成xadmin以便于插件开发
2. 发送邮件等耗时操作使用了Celery任务队列，redis作为操作的中间件，以节约等待时间
3.  记录登陆功能、购物车功能使用了redis缓存存储
4.  admin可以继承save_model方法，而xadmin没有，所以这里使用将关键数据进行比较，如果不相同就说明页面改变，则开启缓存
5. 考虑到服务器的内存可能不够存储静态资源，所以采用了FDFS存储静态资源
6.  将首页，详情页面，列表页等所有用户都能看到的界面在第一次访问之后静态化，以减少数据库的操作
7. 搜索功能采用了haystack全文检索框架来使用whoosh搜索引擎，在搜索的时候使用jieba分词，能使得搜索更全面和准确
8.  订单并发使用了乐观锁来解决并发问题
9.  支付功能使用支付宝的沙箱环境，可以生成支付后的随机字符串

##  开发日志

1. 第一天搭建好所有页面的基本模板，设置好页面的路由，重写了视频中的登陆注册页面，相对比增加了验证失败的表单提示、增加了验证码(django-simple-captcha)功能，修改了视频中写的复杂的验证逻辑，直接用Django内置的form表单验证解决问题，把admin修改成xadmin以便于添加插件，增加了富文本编辑器(DjangoUeditor)
2. 第二天，对邮件发送这个部分采用了celery，celery本身只是一个异步的操作，本身不提供任务队列的功能，可以借助于RabbitMQ或者Redis数据库来操作。因为我的虚拟机搭建celery的worker端有太多的bug，所以我这里采用的是本机系统上使用celery，而且发现我测试注册发送邮件次数太多导致我的ip被封了.......，改了个ip解决问题(开发一个钟，改BUG半天...)
3. 使用redis作为登陆的缓存、使用Minin的方法来增加地址重定向的问题、完成redis记录浏览历史的功能，在阿里云centos7服务器上部署fdfs（大坑，不仅仅控制台要加防火墙规则，内部还要开启端口并且重启防火墙才能生效，改了一下午），并且所有资源都使用fdfs使用文件部署
4. 使用了celery异步缓存首页文件，并且发现在windows上写文件默认的编码是gbk，所以在win10上部署的时候一定要encoding='utf-8'
5. 继承admin有一个save_model方法，如果管理员修改了数据那么就重新定义一次缓存，但因为我这里用的是xadmin，所以不能继承admin的方法，就不能实时修改缓存。然后我想了一个临时解决的办法，在goods的views.py里面判断两次context的值是否相等，如果不相等那么就是后台修改了数据。完成商城的详情、列表页。完成搜索功能。
6. 完成支付宝沙箱环境支付，文档会留在doc文件夹内，沙箱环境的appid不在代码上提供，使用者可以自己申请、使用uwsgi上线网站

## 开发总结

​	这个项目是我看完视频后自己重新写的一个项目，重写了大部分逻辑，这个项目内部逻辑很简单，但是前端方面相比较就难了。这个项目前端页面不利于二次开发，也不好看，所以我打算重构一个全新的前端和移动端作为一个完整的项目。

​	这个项目我重写了大部分逻辑，还留下一些小Bug，因为最近没什么时间改进这个项目，所以先留下一个坑，等我有空了再去改

​	如果对此项目有什么疑问或者想要知道我修改逻辑的地方联系我的邮箱：ly163qfxmn@163.com

​	如果这个项目对你有帮助的话就给个start吧







