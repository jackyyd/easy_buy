"""
首页接口序列化器
"""
from rest_framework import serializers
from apps.goods.models import GoodsVisitCount



class GoodsVisitModelSerializer(serializers.ModelSerializer):
    # 序列化结果是关联对象的主键值
    category = serializers.StringRelatedField()


    class Meta:
        model = GoodsVisitCount
        fields = ['count', 'category']
