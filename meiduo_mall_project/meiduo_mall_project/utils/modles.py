"""
models: 为公共模型类的模块
"""
from django.db import models


class BaseModel(models.Model):
    """
    为模型类补充字段
    """
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name=True)

    class Meta:
        # 说明是抽象模型类（抽象模型类不会创建表）
        abstract = True
