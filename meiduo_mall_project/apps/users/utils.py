"""
utils: 实现用户多种方式登录
"""
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from settings.dev import logger
from .models import User


class AuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except Exception as e:
            logger.warning("获取用户失败：%s", e)
            return None
        if user and user.check_password(password):
            return user
