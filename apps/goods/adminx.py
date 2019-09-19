__author__ = 'LY'
__date__ = '2019/9/13 10:22'
from xadmin import views
from .models import *
import xadmin

class GoodsTypeAdmin(object):
    list_display = ['name', 'logo', 'image']
    search_fields = ['name', 'logo', 'image']
    list_filter = ['name', 'logo', 'image']


class GoodsSKUAdmin(object):
    list_display = ['type', 'goods','name','desc','price','unite','image','stock','sales','status']
    search_fields = ['type', 'goods','name','desc','price','unite','image','stock','sales','status']
    list_filter = ['type', 'goods','name','desc','price','unite','image','stock','sales','status']


class GoodsAdmin(object):
    list_display = ['name', 'detail']
    search_fields = ['name', 'detail']
    list_filter = ['name', 'detail']
    style_fields = {"detail": "ueditor"}


class GoodsImageAdmin(object):
    list_display = ['sku', 'image']
    search_fields = ['sku', 'image']
    list_filter = ['sku', 'image']


class IndexGoodsBannerAdmin(object):
    list_display = ['sku', 'image','index']
    search_fields = ['sku', 'image','index']
    list_filter = ['sku', 'image','index']


class IndexTypeGoodsBannerAdmin(object):
    list_display = ['type', 'sku','display_type','index']
    search_fields = ['type', 'sku','display_type','index']
    list_filter = ['type', 'sku','display_type','index']


class IndexPromotionBannerAdmin(object):
    list_display = ['name', 'image','index','url']
    search_fields = ['name', 'image','index','url']
    list_filter = ['name', 'image','index','url']


xadmin.site.register(GoodsType, GoodsTypeAdmin)
xadmin.site.register(GoodsSKU, GoodsSKUAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
xadmin.site.register(IndexTypeGoodsBanner, IndexTypeGoodsBannerAdmin)
xadmin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)