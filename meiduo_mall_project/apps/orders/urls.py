from django.urls import re_path
from . import views


urlpatterns = [
    # 订单确认
    re_path(r'^orders/settlement/$', views.OrderSettlementView.as_view()),
    # 保存订单
    re_path(r'^orders/commit/$', views.OrderCommitView.as_view()),
]
