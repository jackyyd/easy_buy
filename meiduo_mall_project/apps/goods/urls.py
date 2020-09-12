from django.urls import re_path
from . import views


urlpatterns = [
    # sku商品列表页面
    re_path(r'^list/(?P<category_id>\d+)/skus/$', views.ListView.as_view()),
    re_path(r'^hot/(?P<category_id>\d+)/$', views.HotGoodsView.as_view()),
    # sku搜索,映射的时候无需调用as_view
    re_path(r'^search/$', views.MySearchView()),
]
