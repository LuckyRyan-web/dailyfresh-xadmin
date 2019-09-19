## 运行项目
1. 建议创建一个虚拟环境来运行
   python manage.py startapp dailyfresh
   然后一键安装依赖包
   pip install -r requirements.txt
2. 在setting.py中配置自己的服务器或者虚拟机的ip和端口
3. 在celery_tasks配置自己的服务器或者虚拟机的redis端口，然后使用`celery -A ` 启动celery服务
4. 在使用redis缓存记录的时候看看自己的redis数据库有没有值先，redis-cli -h 127.0.0.1 -p 6379，Flushdb(删除单个数据库的所有键值对)
5. 在自己部署的服务器上，使用[文档](https://blog.csdn.net/busishenren/article/details/83584885)里面的步骤去部署，记得[开放端口](https://www.cnblogs.com/heqiuyong/p/10460150.html)
6. 改写utils.fdfs里面的client.conf的base_path和tracker_server字段

## 开发中参考到的博客
[富文本编辑器的使用][https://www.cnblogs.com/zmdComeOn/p/11345418.html]
[富文本编辑器的使用][https://github.com/zhangfisher/DjangoUeditor]
[xadmin集成UEditor][https://blog.csdn.net/wgpython/article/details/79585205]
[阿里云centos服务器安装python3.6][https://www.cnblogs.com/charles8866/p/8366695.html]
[阿里云centos安装pip3][https://www.centos.bz/2018/03/centos-7%E5%AE%89%E8%A3%85pip3/]
[celery在windows系统运行的问题][https://www.cnblogs.com/springionic/p/10959353.html]
[django-redis使用文档][https://django-redis-chs.readthedocs.io/zh_CN/latest/]

[阿里云centos7服务器安装Nginx](https://blog.csdn.net/qq_32953079/article/details/81975160)

```
补充一下

开启Nginx命令: ./nginx -s stop

刷新Nginx命令: ./nginx -s reload
```

[阿里云Centos7一步一步搭建FastDFS](https://blog.csdn.net/busishenren/article/details/83584885)

[阿里云centos7开启端口](https://www.cnblogs.com/heqiuyong/p/10460150.html)

这里切记，阿里云服务器要先开外面的防火墙规则，然后再去开启内部的端口，然后再重启防火墙才有效

这里切记切记，不要先安装python3在安装fdfs，如果安装了开启防火墙会出问题，也不能使用fdfs通过端口访问，如果已经安装了python3，那么看这里[安装Python3之后防火墙无法启动](https://blog.csdn.net/cenylon/article/details/79954524)






## 技术栈

1. 把admin后台管理修改成xadmin，并且新增了一些插件
2. 登陆注册的验证码
3. 采用了异步发送邮件
4. 登陆采用了redis缓存
5. 文件存储形式改为使用fdfs存储，大大节约了服务器的存储空间

##  开发日志
这个项目是我看完天天生鲜这个项目的实战视频后重新自己做了一个，觉得视频中有些逻辑写的太麻烦，部分逻辑我重写和新增了一些功能

1. 第一天搭建好所有页面的基本模板，设置好页面的路由，重写了视频中的登陆注册页面，相对比增加了验证失败的表单提示、增加了验证码(django-simple-captcha)功能，修改了视频中写的复杂的验证逻辑，直接用Django内置的form表单验证解决问题，把admin修改成xadmin以便于添加插件，增加了富文本编辑器(DjangoUeditor)

2. 第二天，对邮件发送这个部分采用了celery，celery本身只是一个异步的操作，本身不提供任务队列的功能，可以借助于RabbitMQ或者Redis数据库来操作。因为我的虚拟机搭建celery的worker端有太多的bug，所以我这里采用的是本机系统上使用celery，而且发现我测试注册发送邮件次数太多导致我的ip被封了.......，改了个ip解决问题(开发一个钟，改BUG半天...)

3. 使用redis作为登陆的缓存、使用Minin的方法来增加地址重定向的问题、完成redis记录浏览历史的功能，在阿里云centos7服务器上部署fdfs（大坑，不仅仅控制台要加防火墙规则，内部还要开启端口并且重启防火墙才能生效，改了一下午），并且在xadmin上使用fdfs使用文件部署

   



