from django.db import models
from meiduo_mall_project.utils.modles import BaseModel

#
# class (BaseModel):
#     name = models.ForeignKey(, related_name='', on_delete=models., verbose_name='名称', null=True, blank=True)
#     models.CharField(max_length=, unique=True, verbose_name='')
#     models.IntegerField(default=, verbose_name='')
#     models.DecimalField(max_digits=, decimal_places=, verbose_name='')
#     models.BooleanField(default=, verbose_name='')
#     models.TextField(null=True, blank=True, verbose_name='')
#     models.ImageField(max_length=, null=True, blank=True, verbose_name='')
#
#     # 对表进行相关设置
#     class Meta:
#         db_table = 'tb_'
#
#     # 返回
#     def __str__(self):
#         return