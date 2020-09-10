from django.db import models
from meiduo_mall_project.utils.modles import BaseModel
from django.contrib.auth.models import AbstractUser


# 定义用户模型类
# 重写用户类
class User(AbstractUser):

    # 增加mobile字段
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    # 增加email_active字段，用于验证邮箱是否被激活，默认是Flase,未激活
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    # 增加default_address字段
    default_address = models.ForeignKey('Address', related_name='users',
                                        null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='默认收货地址')

    # 对表进行相关设置
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = 'verbose_name'

    # 返回用户名称
    def __str__(self):
        return self.username


# 定义用户收货地址模型类
class Address(BaseModel):
    """在数据库中建表tb_address"""

    # 增加字段
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.CASCADE,
                                 related_name='province_address', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.CASCADE,
                             related_name='city_address', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.CASCADE,
                                 related_name='district_address', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='详细地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    # 对tb_address进行设置
    class Meta:
        db_table = 'tb_address'
        # 设置默认时间为降序
        ordering = ['-update_time']
