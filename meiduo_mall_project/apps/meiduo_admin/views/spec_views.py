from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SPUSpecification, SpecificationOption
from ..serializers.spec_serializers import SpecModelSerializer, OptionModelSerializer, OptSpecSimpleSerializer
from ..paginations import MyPage
from rest_framework.generics import ListAPIView


class SpecView(ModelViewSet):
    queryset = SPUSpecification.objects.order_by('id')
    serializer_class = SpecModelSerializer
    pagination_class = MyPage


class OptionView(ModelViewSet):
    queryset = SpecificationOption.objects.order_by('id')
    serializer_class = OptionModelSerializer
    pagination_class = MyPage


class OptSpecSimpleView(ListAPIView):
    queryset = SPUSpecification.objects.order_by('id')
    serializer_class = OptSpecSimpleSerializer
