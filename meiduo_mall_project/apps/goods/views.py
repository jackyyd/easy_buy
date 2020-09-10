from django.views import View
from django.conf import settings
from django.http import JsonResponse

# 定义类视图
class View(View):
    """"""
    def (self, request):
        # 1. 接受参数
        # 2. 校验参数
        # 3. 业务处理
        try:
        except Exception as e:
            settings.logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '错误'
            }, status=400)
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
        })
