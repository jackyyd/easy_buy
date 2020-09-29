from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from ..serializers.sku_serializers import *
from ..paginations import MyPage
from apps.goods.models import SKU, GoodsCategory
from rest_framework.generics import ListAPIView


class SKUGoodsView(ModelViewSet):
    queryset = SKU.objects.order_by('id')
    serializer_class = SKUModelSerializer
    pagination_class = MyPage

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name=keyword)


class SKUCategoryView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = SKUCategorySimpleSerialzier

    def get_queryset(self):
        # 过滤三级分类
        return self.queryset.filter(parent_id__gte=37)


class SPUSimpleView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer


class SPUSpecView(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SPUSpecModelSerializer

    def get_queryset(self):
        # 根据路径中的spu_id过滤出其关联的多个规格数据
        # 命名分组正则提取出来的参数，封装在self.kwargs中(是一个字典,
        # 分组名作为key,提取的传值作为value), 非命名分组正则提取出来的参数,
        # 封装在self.args中(是一个列表,　按照分组顺序提取参数)
        spu_id = self.kwargs.get('pk')
        return self.queryset.filter(spu_id=spu_id)
