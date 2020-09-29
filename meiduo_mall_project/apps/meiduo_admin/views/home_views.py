"""
首页数据（用户和商品）统计
"""

from django.utils import timezone
from datetime import timedelta

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.users.models import User
from rest_framework.response import Response
from datetime import datetime
from apps.orders.models import OrderInfo
from ..serializers.homeserializers import *


# 统计用户总数量
class UserTotalCountView(APIView):
    def get(self, request):
        # 1、接收参数
        # 2、校验参数
        # 3、数据处理-->user.count
        count = User.objects.count()
        # 4、构建响应
        cur_date2 = datetime.today()
        cur_date1 = datetime.now()  # 系统本地时间
        cur_date = timezone.localtime()  # 获取配置参数TIME_ZONE指定时区的时间，返回datetime对象
        return Response({
            'count': count,
            'date': cur_date.date()  # 年月日datetime().date()-->把datetime类型转化为date类型(只取年月日）
        })


# 统计每天增加的用户数量
class UserDayCountView(APIView):
    def get(self, request):
        # 1、接收参数
        # 2、校验参数
        # 3、数据处理-->user.date_joined
        cur_date = timezone.localtime()
        cur_0_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        count = User.objects.filter(date_joined__gte=cur_0_date).count()
        # 4、构建响应
        return Response({
            'count': count,
            'date': cur_date.date()
    })


# 统计每天活跃的用户数量
class UserActiveCountView(APIView):
    def get(self, request):
        # 1、接收参数
        # 2、校验参数
        # 3、数据处理--user.last_login
        cur_0_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        count = User.objects.filter(last_login__gte=cur_0_date).count()
        # 4、构建响应
        return Response({
            'count': count,
            'date': cur_0_date.date()
        })



# 统计每天下单的用户数量
class UserOrderCountView(APIView):
    def get(self, request):
        #　1、接收参数
        # 2、校验参数
        # 3、数据处理-->1.从从表出发2.从主表出发(两张表问题)
        cur_date = timezone.localtime()
        cur_0_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        # orders = OrderInfo.objects.filter(create_time__gte=cur_0_date)
        # users = set()
        # for order in orders:
        #     users.add(order.user)
        # orders = OrderInfo.objects.filter(create_time__gte=cur_0_date)
        # count = len(set([order.user_id for order in orders]))
        users = User.objects.filter(orders__create_time__gte=cur_0_date)
        count = len(users)
        # 4、构建响应
        return Response({
            'count': count,
            'date': cur_date.date()
        })


# 统计每月每天增加的用户数量
class UserMonthCountView(APIView):
    def get(self, request):
        # 1、接收参数
        # 2、校验参数
        # 3、数据处理-->1.30天如何表示;2.30天的其中一天如何表示
        # 30天最后一天0时刻
        end_0_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        #  30天第一天0时刻
        start_0_date = end_0_date - timedelta(days=29)
        ret_list = []
        for index in range(30):
            # cur_0_date = start_0_date + timedelta(days=0)  # 第一天
            # cur_0_date = start_0_date + timedelta(days=1)  # 第二天
            cur_0_date = start_0_date + timedelta(days=index)  # 其中某一天的零时刻
            next_0_date = cur_0_date + timedelta(days=1)  # 某一天后一天的零时刻
            count = User.objects.filter(date_joined__gte=cur_0_date, date_joined__lt=next_0_date).count()
            ret_list.append({
                "count": count,
                "date": cur_0_date.date()
            })
        # 4、构建响应
        return Response(ret_list)


# 统计每天各类商品的访问数量
class GoodsDayView(ListAPIView):
        # 1. 接收参数
        # 2. 校验参数
        # 3. 数据处理-->GoodVisitCount
        # 如果在类属性中获取0时刻,这个cur_0_time记录的永远都是服务器启动的那一天的时刻了
        # cur_0_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        # query_set = GoodsVisitCount.objects.filter(create_time__gte=cur_0_date)
        queryset = GoodsVisitCount.objects.all()
        serializer_class = GoodsVisitModelSerializer

        # 4. 构建响应
        # 在每一次请求的时候都通过get_queryset()方法来获取查询集
        def get_queryset(self):
            cur_0_date = timezone.localtime().replace(hour=0, minute=0, second=0)
            return self.queryset.filter(
                create_time__gte=cur_0_date
            )
