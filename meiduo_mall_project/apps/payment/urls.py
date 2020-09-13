from django.urls import re_path
from . import views


urlpatterns = [
    # 支付宝支付网址: GET /payment/(?P<order_id>\d+)/
    re_path(r'^payment/(?P<order_id>\d+)/$', views.PaymentView.as_view()),
    # 处理支付成功的回调: PUT /payment/status/
    re_path(r'^payment/status/$', views.PaymentStatusView.as_view()),
]
