# 导包
from django.db import models
from django.contrib.auth.models import AbstractUser


# 重写用户类
class User(AbstractUser):

    # 增加mobile字段
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    # 对表进行相关设置
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = 'verbose_name'

    # 返回用户名称
    def __str__(self):
        return self.username
