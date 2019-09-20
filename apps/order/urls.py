__author__ = 'LY'
__date__ = '2019/9/20 19:31'
from django.conf.urls import url
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView, OrderCommentView

urlpatterns = [
    url(r'^place$', OrderPlaceView.as_view(), name='place'),  # 提交订单显示
    url(r'^commit$', OrderCommitView.as_view(), name='commit'),  # 订单创建
    url(r'^pay$', OrderPayView.as_view(), name='pay'),  # 订单支付
    url(r'^check$', CheckPayView.as_view(), name='ckeck'),  # 查询支付交易结果
    url(r'^comment/(?P<order_id>.+)$', OrderCommentView.as_view(), name='comment'),  # 订单评论
]
