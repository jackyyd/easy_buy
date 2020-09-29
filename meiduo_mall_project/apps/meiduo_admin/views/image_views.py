from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage
from ..serializers.image_serializers import ImageModelSerializer
from ..paginations import MyPage


class ImageView(ModelViewSet):
    queryset = SKUImage.objects.order_by('id')
    serializer_class = ImageModelSerializer
    pagination_class = MyPage