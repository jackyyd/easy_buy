from django.db import models
from meiduo_mall_project.utils.modles import BaseModel


# 定义QQ登录模型类
class OAuthQQUser(BaseModel):
    """
    QQ登录用户数据
    """
    # user是个外键，关联对应的用户
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    # QQ发布的用户身份id
    openid = models.CharField(max_length=164, verbose_name='openid', db_index=True)

    class Meta:
        # 数据库表名为tb_oauth_qq
        db_table = 'tb_oauth_qq'
