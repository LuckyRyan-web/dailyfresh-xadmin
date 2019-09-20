from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from dailyfreshshop.settings import SECRET_KEY,EMAIL_FROM
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email
from .forms import *
from .models import *
from goods.models import *
from base.mixin import *
from django_redis import get_redis_connection
import re


class RegisterView(View):

    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        username = request.POST.get('registerUsername', '')
        password1 = request.POST.get('registerPassword', '')
        password2 = request.POST.get('registerPasswords', '')
        email = request.POST.get('registeremail', '')
        if password1 == password2:
            password = password1
        else:
            return render(request, 'register.html', {'error': "两次密码不一致，请重新填写"})

        if not all([username, password, email]):  # all可以自动验证数据是否完整
            return render(request, 'register.html', {'errormsg': '数据不完整，请重新填写'})

        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            if User.objects.filter(email=email):
                return render(request, "register.html", {"register_form": register_form, "email_msg": "邮箱已注册"})
            if User.objects.filter(username=username):
                return render(request, "register.html", {"register_form": register_form, "user_msg": "用户名已存在"})

            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()

            #加密用户的id发送链接
            serializer = Serializer(SECRET_KEY, 180)
            info = {'confirm':user.id}
            token=serializer.dumps(info)
            token = token.decode('utf8')

            # email_title = "天天生鲜注册激活链接"
            # email_body = ''
            # sender = EMAIL_FROM
            # receiver = [email]
            # html_message = "<h1>%s，欢迎您注册天天生鲜商城，请点击下面的连接激活你的账号</h1>" \
            #                "<a href='http://127.0.0.1:8000/active/%s'>http://127.0.0.1:8000/active/%s</a>" % (
            #                    username, token, token)
            # send_mail(email_title, email_body, sender, receiver, html_message=html_message)

            send_register_active_email.delay(email, username, token)

            return HttpResponse('邮箱验证码已经发送到您的邮箱，请点击连接激活')
        else:
            return render(request, 'register.html', {'msg': '表单不准确'})


class LoginView(View):
    def get(self,request):
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
            checked='checked'
        else:
            username=''
            checked=''
        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        if not all([username,password]):
            return render(request, 'login.html', {'errormsg': '数据不完整，请重新填写'})
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)                                         #login方法是Django后台自定义的登陆方法，内置了cookie和session的方法

                    #默认登陆后跳转到首页
                    next_url=request.GET.get('next',reverse('goods:index'))

                    response=redirect(next_url)

                    #判断是否记住用户名
                    remember=request.POST.get('remember')

                    if remember == "on":
                        response.set_cookie('username',username,max_age=7*24*3600)
                    else:
                        response.delete_cookie('username')

                    return response
                else:
                    return render(request,"login.html",{"email_msg":"你的邮箱未激活"})
            else:
                return render(request,'login.html',{"user_msg":"用户名或密码错误"})
        else:
            return render(request,"login.html",{"login_form":login_form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('goods:index'))


class AciveUserView(View):
    def get(self,request,token):
        serializer = Serializer(SECRET_KEY, 180)
        try:
            info=serializer.loads(token)
            #获取info的用户id
            user_id=info['confirm']
            #根据id来获取用户信息
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            return redirect(reverse('login'))
        except SignatureExpired as e:
            #激活链接过期了
            return HttpResponse('激活链接过期，请重新提交')


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        address = Address.objects.get_default_address(user)

        #获取浏览记录
        con=get_redis_connection('default')
        history_key='history_%d'%user.id
        sku_ids=con.lrange(history_key,0,4)

        goods_list = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_list.append(goods)

        # 组织上下文
        context = {'page': 'user',
                   'address': address,
                   'goods_list': goods_list}

        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'user_center_order.html',{'page':'order'})


class UserAddressView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None  # 不存在默认地址
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html',
                      {'title': '用户中心-收货地址', 'page': 'address', 'address': address})

    def post(self, request):
        # 地址添加
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 业务处理：地址添加
        # 如果用户没存在默认地址，则添加的地址作为默认收获地址
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None  # 不存在默认地址
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 数据校验
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html',
                          {'page': 'address',
                           'address': address,
                           'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1([3-8][0-9]|5[189]|8[6789])[0-9]{8}$', phone):
            return render(request, 'user_center_site.html',
                          {'page': 'address',
                           'address': address,
                           'errmsg': '手机号格式不合法'})

        # 添加
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答
        return redirect(reverse('user:address'))  # get的请求方式