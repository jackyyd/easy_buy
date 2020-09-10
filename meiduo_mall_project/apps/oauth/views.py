import json
import re
from django.contrib.auth import login
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection
from meiduo_mall_project.utils.secret import SecretOauth
from apps.users.models import User
from django.conf import settings
from .models import OAuthQQUser
from meiduo_mall_project.utils.oauth import oauth


class QQURLView(View):
    """
    获取QQ登录页面网址
    """
    def get(self, request):
        # 01. 提取数据
        # next记录QQ登录成功后进入的网址
        next = request.GET.get('next')
        # 02. 校验数据
        # 03. 数据处理
        # 获取QQ登录页面网址
        login_url = oauth.get_qq_url()
        # 04. 返回响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'OK',
            'login_url': login_url
        })


# 定义QQ登陆回调类
class QQUserView(View):
    """
    实现用户登陆回调接口
    """
    def get(self, request):
        # 1. 接受参数
        # 浏览器向美多发送code
        code = request.GET.get('code')
        # 2. 校验参数
        if not code:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少参数'
            })
        # 3. 数据处理
        try:
            # 3.1 携带code获得access_token
            access_token = oauth.get_access_token(code)
            # 3.2 携带access_token获得open_id
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            # 如果上面获取 openid 出错, 则验证失败
            settings.logger.error(e)
            # 返回结果
            return JsonResponse({'code': 400, 'errmsg': 'oauth2.0认证失败, 即获取qq信息失败'})

        # 3.3.1
        try:
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果 openid 没绑定美多商城用户,进入这里:
            # 使用加密类加密 openid
            access_token = SecretOauth().dumps({'openid': openid})
            # 注意: 这里一定不能返回 0 的状态码. 否则不能进行绑定页面
            return JsonResponse({'code': 300, 'errmsg': 'ok', 'access_token': access_token})
        else:
            # 如果 openid 已绑定美多商城用户
            # 根据 user 外键, 获取对应的 QQ 用户(user)
            user = oauth_qq.user

            # 实现状态保持
            login(request, user)

            # 创建重定向到主页的对象
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})

            # 将用户信息写入到 cookie 中，有效期14天
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)

            # 返回响应
            return response
        # 4. 返回响应

    def post(self, request):
        """美多商城用户绑定到openid"""

        # 1.接收参数
        data_dict = json.loads(request.body.decode())
        mobile = data_dict.get('mobile')
        password = data_dict.get('password')
        sms_code_client = data_dict.get('sms_code')
        access_token = data_dict.get('access_token')

        # 2.校验参数
        # 判断参数是否齐全
        if not all([mobile, password, sms_code_client]):
            return JsonResponse({'code': 400,
                                'errmsg': '缺少必传参数'})

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                'errmsg': '请输入正确的手机号码'})

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400,
                                'errmsg': '请输入8-20位的密码'})

        # 3.判断短信验证码是否一致
        # 创建 redis 链接对象:
        redis_conn = get_redis_connection('verify_code')

        # 从 redis 中获取 sms_code 值:
        sms_code_server = redis_conn.get('sms_%s' % mobile)

        # 判断获取出来的有没有:
        if sms_code_server is None:
            # 如果没有, 直接返回:
            return JsonResponse({'code': 400,
                                'errmsg': '验证码失效'})
        # 如果有, 则进行判断:
        if sms_code_client != sms_code_server.decode():
            # 如果不匹配, 则直接返回:
            return JsonResponse({'code': 400,
                                'errmsg': '输入的验证码有误'})

            # 调用我们自定义的函数, 检验传入的 access_token 是否正确:
        # 错误提示放在 sms_code_errmsg 位置
        openid = SecretOauth().loads(access_token).get('openid')
        if not openid:
            return JsonResponse({'code': 400,
                                'errmsg': '缺少openid'})
        # 4.保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(password):
                return JsonResponse({'code': 400,
                                    'errmsg': '输入的密码不正确'})
        # 5.将用户绑定 openid
        try:
            OAuthQQUser.objects.create(openid=openid,
                                       user=user)
        except Exception as e:
            settings.logger(e)
            return JsonResponse({'code': 400,
                                'errmsg': '往数据库添加数据出错'})
        # 6.实现状态保持
        login(request, user)

        # 7.创建响应对象:
        response = JsonResponse({'code': 0,
                                'errmsg': 'ok'})

        # 8.登录时用户名写入到 cookie，有效期14天
        response.set_cookie('username',
                            user.username,
                            max_age=3600 * 24 * 14)

        # 9.响应
        return response
