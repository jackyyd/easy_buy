from django.urls import re_path
from .views.login_views import *
from rest_framework_jwt.views import obtain_jwt_token
from .views.home_views import *
urlpatterns = [
    # re_path(r'^authorizations/$', LoginView.as_view()),
    re_path(r'^authorizations/$', obtain_jwt_token),
    # 1、用户总数统计
    re_path(r'^statistical/total_count/$', UserTotalCountView.as_view()),
    # 2、统计当日新增用户
    re_path(r'^statistical/day_increment/$', UserDayCountView.as_view()),
    # 3、统计当日活跃用户
    re_path(r'^statistical/day_active/$', UserActiveCountView.as_view()),
    # 4、统计当日下单用户
    re_path(r'^statistical/day_orders/$', UserOrderCountView.as_view()),
    # 5、统计当日分类商品访问量月增用户
    re_path(r'^statistical/month_increment/$', UserMonthCountView.as_view()),
    # 6、统计当日分类商品访问量
    re_path(r'^statistical/goods_day_views/$', GoodsDayView.as_view()),

]
