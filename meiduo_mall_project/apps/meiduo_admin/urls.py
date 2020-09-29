"""
美多后台路由
"""

from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token
from .views.login_views import *
from .views.home_views import *
from .views.user_views import *
from .views.sku_views import *
from .views.spu_views import *
from .views.spec_views import *
from .views.image_views import *


urlpatterns = [
    # 登陆
    # re_path(r'^authorizations/$', LoginView.as_view()),
    re_path(r'^authorizations/$', obtain_jwt_token),
    # 统计用户总量
    re_path(r'^statistical/total_count/$', UserTotalCountView.as_view()),
    # 统计每天增加的用户数量
    re_path(r'^statistical/day_increment/$', UserDayCountView.as_view()),
    # # 统计每天活跃的用户数量
    re_path(r'^statistical/day_active/$', UserActiveCountView.as_view()),
    # # 统计每天下单的用户数量
    re_path(r'^statistical/day_orders/$', UserOrderCountView.as_view()),
    # # 统计每月每天增加的用户数量
    re_path(r'^statistical/month_increment/$', UserMonthCountView.as_view()),
    # # 统计每天用户访问的商品数量
    re_path(r'^statistical/goods_day_views/$', GoodsDayView.as_view()),
    # 获取查询用户
    re_path(r'^users/$', UserView.as_view()),
    # SKU管理
    # re_path(r'^skus/$', SKUGoodsView.as_view({'get': 'list'})),
    # 新增SKU可选的三级分类
    re_path(r'^skus/categories/$', SKUCategoryView.as_view()),
    # 新增SKU的可选SPU
    re_path(r'^goods/simple/$', SPUSimpleView.as_view()),
    # 新增SKU的可选规格和选项信息
    re_path(r'^goods/(?P<pk>\d+)/specs/$', SPUSpecView.as_view()),
    # sku关联
    re_path(r'^skus/$', SKUGoodsView.as_view({'get': 'list', 'post': 'create'})),
    # SKU管理
    re_path(r'^skus/(?P<pk>\d+)/$', SKUGoodsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # SPU管理
    re_path(r'^goods/$', SPUGoodsView.as_view({'get': 'list','post':'create'})),
    re_path(r'goods/(?P<pk>\d+)/$', SPUGoodsView.as_view(
        {'get': 'retrieve',
         'put': 'update',
         'delete': 'destroy'})),
    # 新增SPU可选品牌
    re_path(r'^goods/brands/simple/$', SPUBrandView.as_view()),
    # 新增SPU可选一级分类
    re_path(r'^goods/channel/categories/$', SPUCategoryView.as_view()),
    # 新额增SPU可选二级或者三级分类,
    re_path(r'^goods/channel/categories/(?P<pk>\d+)/$', SPUCategoryView.as_view()),
    # 规格管理
    re_path(r'^goods/specs/$', SpecView.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^goods/specs/(?P<pk>\d+)/$', SpecView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })),
    # 选项管理
    re_path(r'^specs/options/$', OptionView.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^specs/options/(?P<pk>\d+)/$', OptionView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新增选项可选规格
    re_path(r'^goods/specs/simple/$', OptSpecSimpleView.as_view()),
    # 图片管理
    re_path(r'^skus/images/$', ImageView.as_view()),
]
