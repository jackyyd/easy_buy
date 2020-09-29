from rest_framework import serializers
from apps.goods.models import SKUImage


class ImageModelSerializer(serializers.ModelSerializer):
    sku = serializers.StringRelatedField()

    class Meta:
        model = SKUImage
        fields = [
            'id',
            'sku',
            'image'
        ]

    def validate(self, attrs):
        image_obj = attrs.get('image')
        conn = Fdfs_client
