from django.views import View
from apps.areas.models import Area
from meiduo_mall_project.utils.logger import logger
from django.http import JsonResponse


# 定义省区类视图
class ProvinceAreasView(View):
    """获取省区数据接口"""
    def get(self, request):
        # 1. 接受参数
        # 2. 校验参数
        # 3. 业务处理
        try:
            # 3.1 查询省级数据
            province_model_list = Area.objects.filter(parent__isnull=True)
            # 3.2 整理省级数据
            province_list = []
            for province_model in province_model_list:
                province_list.append({
                    'id': province_model.id,
                    'name': province_model.name
                })
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '省区数据错误'
            })
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'province_list': province_list
        })


# 定义市区类视图
class SubAreasView(View):
    """获取市或区数据"""
    def get(self, request, pk):
        # 1. 接收参数
        # 2. 校验参数
        # 3. 业务处理
        try:
            # 3.1 获取市区数据
            sub_model_list = Area.objects.filter(parent=pk)
            # 3.2 获取省区数据
            parent_model = Area.objects.get(id=pk)
            # 3.2 整理市区数据
            sub_list = []
            for sub_model in sub_model_list:
                sub_list.append({
                    'id': sub_model.id,
                    'name': sub_model.name
                })
            sub_data = {
                'id': parent_model.id,
                'name': parent_model.name,
                'subs': sub_list
            }
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '市或区数据错误'
            })
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'sub_data': sub_data
        })
