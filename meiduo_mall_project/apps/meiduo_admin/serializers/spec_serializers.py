from rest_framework import serializers
from apps.goods.models import SPUSpecification, SpecificationOption


class SpecModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name',
            'spu',
            'spu_id'
        ]


class OptionModelSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption
        fields = [
            'id',
            'value',
            'spec',
            'spec_id'
        ]


class OptSpecSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        fields = [
            'id',
            'name'
        ]
