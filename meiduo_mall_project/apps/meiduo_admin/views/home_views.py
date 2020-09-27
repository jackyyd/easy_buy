from datetime import date, timedelta
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User


class UserTotalCountView(APIView):
    def get(self, request):
        count = User.objects.count()
        cur_date = timezone.localtime()
        return Response({
            'count': count,
            'date': cur_date.date()
        })


class UserDayCountView(APIView):
    def get(self, request):
        cur_time = timezone.localtime()
        cur_0_time = cur_time.replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(
            date_joined__gte=cur_0_time
        ).count()

        return Response({
            'count': count,
            'date': cur_time.date()
    })


class UserActiveCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date=timezone.localtime().replace(hour=0, minute=0, second=0)
        # 获取当前登陆用户数量
        count = User.objects.filter(last_login__gte=now_date).count()
        return Response({
            'count': count,
            'date': now_date
        })


class UserOrderCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date=timezone.localtime().replace(hour=0, minute=0, second=0)
        # 获取当前下单用户数量 orders__create_time 订单创建时间
        count = User.objects.filter(orders__create_time__gte=now_date).count()
        return Response({
            "count": count,
            "date": now_date
        })


class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        # 获取一个月前日期
        start_date = now_date - timedelta(29)
        # 创建空列表保存每天的用户量
        date_list = []
        for i in range(30):
            # 循环遍历获取当前日期
            index_date = start_date + timedelta(days=i)
            # 指定下一天日期
            cur_date = start_date + timedelta(days=i + 1)
            # 查询条件是大于当前日期index_date,小于明天日期的用户cur_date,等到当前用户量
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()

            date_list.append({
                'count': count,
                'date': index_date
            })
        return Response(date_list)


class GoodsDayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request):
        now_date = timezone.localtime().replace(hour=0, minute=0, second=0)
        start_date = now_date - timedelta(29)
        date_list = []

        for i in range(30):
            index_date = start_date + timedelta(days=i)
            cur_date = start_date + timedelta(days=i + 1)
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()

            date_list.append({
                'count': count,
                'date': index_date
            })
        return Response(date_list)

