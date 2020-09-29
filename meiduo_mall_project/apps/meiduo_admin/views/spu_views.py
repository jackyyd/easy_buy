from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from apps.goods.models import SPU
from ..serializers.spu_serializers import *
from ..paginations import *


class SPUGoodsView(ModelViewSet):
    queryset = SPU.objects.all()
    serializer_class = SPUGoodsSerialzier
    pagination_class = MyPage

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.get(name__contains=keyword)
        return self.queryset.all()



class SPUBrandView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = SPUBrandSerizliser


class SPUCategoryView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = SPUCategorySerizliser

    def get_queryset(self):
        parent_id = self.kwargs.get('pk')
        if parent_id:
            return self.queryset.filter(parent_id=parent_id)
        return self.queryset.filter(parent_id=None)

