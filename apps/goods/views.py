from django.shortcuts import render
from .models import *
from django.views.generic.base import View
from django.core.cache import cache
from django_redis import get_redis_connection
from utils.hash_file import *
from celery_tasks.tasks import generate_static_index_html

class IndexView(View):
    """首页"""
    def get(self, request,html):
        """显示"""
        # 先判断缓存中是否有数据,没有数据不会报错返回None
        context = cache.get('index_page_data')

        if context is None:
            # 查询商品的分类信息
            types = GoodsType.objects.all()
            # 获取首页轮播的商品的信息
            index_banner = IndexGoodsBanner.objects.all().order_by('index')
            # 获取首页促销的活动信息
            promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

            # 获取首页分类商品信息展示
            for type in types:
                # 查询首页显示的type类型的文字商品信息
                title_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
                # 查询首页显示的图片商品信息
                image_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 动态给type对象添加两个属性保存数据
                type.title_banner = title_banner
                type.image_banner = image_banner

            # 组织上下文
            context = {
                'types': types,
                'index_banner': index_banner,
                'promotion_banner': promotion_banner,
            }

            # 设置缓存数据,缓存的名字，内容，过期的时间
            cache.set('index_page_data', context, 3600)

        # 使用md5加密来计算哈希值
        html_page = cache.get('index_html_data')
        html = mdfive(context)
        if html_page is None:
            cache.set('index_html_data', html, 3600)
        else:
            if html==html_page:
                pass
            else:
                generate_static_index_html.delay()


        # 获取user
        user = request.user
        # 获取登录用户的额购物车中的商品的数量
        cart_count = 0
        if user.is_authenticated:
            # 用户已经登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            # 获取用户购物车中的商品条目数
            cart_count = conn.hlen(cart_key)  # hlen hash中的数目

            context.update(cart_count=cart_count)

        return render(request, 'index.html', context)