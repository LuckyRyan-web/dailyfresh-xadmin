__author__ = 'LY'
__date__ = '2019/9/18 0:15'
from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns=[
    url(r'^$', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    url(r'^address/$', UserAddressView.as_view(), name='address'),  # 用户中心-地址页
]