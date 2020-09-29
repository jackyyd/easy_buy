from rest_framework import serializers
from apps.goods.models import SPU, Brand, GoodsCategory


class SPUGoodsSerialzier(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()  # 默认是read_only=True
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    class Meta:
        model = SPU
        fields = [
            'id',
            'name',
            'brand',
            'brand_id',
            'category1_id',
            'category2_id',
            'category3_id',
            'scales',
            'comments',
            'desc_detail',
            'desc_pack',
            'desc_service'
        ]


class SPUBrandSerizliser(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name'
        ]


class SPUCategorySerizliser(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = [
            'id',
            'name'
        ]
