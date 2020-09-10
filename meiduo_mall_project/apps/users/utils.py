"""
utils: 实现用户多种方式登录
"""
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from meiduo_mall_project.settings.dev import logger
from .models import User
from meiduo_mall_project.utils.secret import SecretOauth
from django.conf import settings


class AuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except Exception as e:
            logger.warning("获取用户失败：%s", e)
            return None
        if user and user.check_password(password):
            return user


# 生成连接激活码
def generate_verify_email_url(request):
    # 1. user_id.mail
    data_dict = {
        'user_id': request.user.id,
        'email': request.user.email
    }
    # 2. 数据加密
    dumps_data = SecretOauth().dumps(data_dict)
    # 3. 拼接完整的激活路由
    verify_url = settings.EMAIL_VERIFY_URL + dumps_data
    return verify_url
