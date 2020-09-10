from django.db import models


# 定义areas模型类视图
class Area(models.Model):
    # 创建name字段，用户保存名称
    name = models.CharField(max_length=20, verbose_name='名称')
    # 创建关联字段parent
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs',
                               null=True, blank=True, verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
