from rest_framework.generics import ListCreateAPIView
from ..serializers.userserializers import *
from ..paginations import MyPage


class UserView(ListCreateAPIView):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserModelSerializer
    pagination_class = MyPage


    def get_queryset(self):
        # 1. 提取keyword
        # 根据查询字符串参数keyword过滤
        # drf中,request可以传入视图函数,还会封装到self.request中(self指的是视图对象)
        keyword = self.request.query_params.get('keyword')
        # 2. 根据keyword过滤
        if keyword:
            return self.queryset.filter(username__contains=keyword)
        return self.queryset.all()  # 获取新数据
