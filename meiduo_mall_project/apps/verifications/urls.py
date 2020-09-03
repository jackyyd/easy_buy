from django.urls import path

from . import views


urlpatterns = [
    path('image_codes/<uuid:uuid>/', views.ImageCodeView.as_view()),
    # 获取短信验证码的子路由:
    path('sms_codes/<mobile:mobile>/', views.SMSCodeView.as_view())
]
