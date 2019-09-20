"""dailyfreshshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from user.views import *
from goods.views import IndexView
import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),  # 富文本编辑器
    url('search/', include('haystack.urls')),  # 全文检索框架
    url(r'^captcha/', include('captcha.urls')),         # 验证码
    url(r'', include('goods.urls', namespace='goods')),  # 商品模块
    url('cart/', include('cart.urls', namespace='cart')),  # 购物车模块
    # url('order/', include('order.urls', namespace='order')),  # 订单模块
    # url(r'^index/$|index.html/$|^$', IndexView.as_view(), name='index'),
    url(r'^active/(?P<token>.*)$', AciveUserView.as_view(), name='active'),  # 用户激活
    url(r'^user/',include('user.urls',namespace='user')),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]
