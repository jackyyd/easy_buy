from django.urls import re_path
from . import views


urlpatterns = [
    # 添加购物车
    re_path(r'^carts/$', views.CartsView.as_view()),
    # 全选/取消购物车
    re_path(r'^carts/selection/$', views.CartsSelectAllView.as_view()),
    # 展示购物车简图
    re_path(r'^carts/simple/$', views.CartsSimpleView.as_view()),
]
