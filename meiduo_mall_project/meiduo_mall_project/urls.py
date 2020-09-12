"""meiduo_mall_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# 总路由中注册路由转换器
from django.urls import register_converter
from meiduo_mall_project.utils import converters


register_converter(converters.UsernameConverter, 'username')
register_converter(converters.MobileConverter, 'mobile')
urlpatterns = [
    path('admin/', admin.site.urls),
    # 添加apps总路由
    path('', include('apps.users.urls')),
    # 添加verifications总路由
    path('', include('apps.verifications.urls')),
    # 添加oauth总路由
    path('', include('apps.oauth.urls')),
    # 地区总路由
    re_path(r'', include('apps.areas.urls')),
    # 商品
    re_path(r'', include('apps.goods.urls')),
    # 购物车
    re_path(r'', include('apps.carts.urls')),
    # 订单
    re_path(r'', include('apps.orders.urls')),
]
