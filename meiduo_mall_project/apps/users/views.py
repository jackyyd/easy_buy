from django.views import View
import json
import re
from django import http
from django.contrib.auth import login

from django_redis import get_redis_connection

from apps.verifications.libs.yuntongxun.sms import CCP
from apps.verifications.libs.captcha.captcha import captcha

# 注意User的导包路径
from apps.users.models import User
from settings.dev import logger


# 定义用户名类视图
class UsernameCountView(View):
    """
    判断用户名是否重复注册
    """
    def get(self, request, username):
        # 查询username在数据库中的个数
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:

            return http.JsonResponse({'code': 400, 'errmsg': '访问数据库失败'})
        # 返回结果(json)-->code & errmsg &count
        return http.JsonResponse({'code': 0, 'errmsg':'ok', 'count':count})


# 定义手机号类视图
class MobileCountView(View):
    """
    判断手机号是否重复注册
    """
    # 1. 获取参数
    def get(self, request, mobile):
        # 异常处理
        try:
            # 判断手机号是否重复（数据处理）
            count = User.objects.filter(mobile = mobile).count()
        except Exception as e:
            return http.JsonResponse({
                'code': 0,
                'errmsg': '查询数据库出错'
            })
        # 构建响应
        return http.JsonResponse({
            'code': 400,
            'errmsg': 'ok',
            'count': count
        })


# 定义用户注册接口


class RegisterView(View):

    def post(self, request):
        '''接收参数, 保存到数据库'''
         # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode() # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str) # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())

        # 提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        allow = json_dict.get('allow')
        sms_code = json_dict.get('sms_code')

        # 2.校验(整体参数是否为空)
        if not all([username, password, password2, mobile, sms_code]):
            return http.JsonResponse({'code':400, 'errmsg':'缺少必传参数!'})

        # 3.username检验
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})

        # 4.password检验
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})

        # 5.password2 和 password
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 6.mobile检验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 7.allow检验
        if allow != True:
            return http.JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})


        # 8.注册的核心逻辑-保存到数据库 (username password mobile)
        try:
            user =  User.objects.create_user(username=username,
                                             password=password,
                                             mobile=mobile)
        except Exception as e:
            return http.JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        login(request, user)
        # 13.拼接json返回
        return http.JsonResponse({'code': 0, 'errmsg': '注册成功!'})
