#!/usr/bin/env python
# 添加Python脚本导包路径
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(2, BASE_DIR)
# 加载django程序的环境
# 设置django运行所需要的环境
os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall_project.settings.dev'
# django初始化
import django
django.setup()
from apps.contents.crons import *
from apps.goods.utils import *
from apps.goods.models import SKU
from django.template import loader
from django.conf import settings


def generate_static_sku_detail_html(sku):
    """
    生成指定sku商品的详情页面
    :param sku_id:
    :return:
    """
    # 查询商品频道分类
    categories = get_categories()
    # 查询当前商品规格
    goods, sku, specs = get_goods_and_spec(sku.id)
    # 1. 获得模板
    template = loader.get_template('detail.html')
    # 2. 设置参数
    context = {
        'categories': categories,
        'goods': goods,
        'sku': sku,
        'specs': specs
    }
    # 3. 渲染页面
    page = template.render(context)
    # 4. 写入文件
    file_path = os.path.join(settings.STATIC_FILE_PATH,
                             'goods/%d.html' % sku.id)
    with open(file_path, 'w',) as f:
        f.write(page)


# 脚本入口
if __name__ == '__main__':
    # 获取所有上架的sku信息
    skus = SKU.objects.filter(is_launched=True)
    # 遍历skus得到sku,利用generate_static_sku_detail_html函数生成对应的页面
    for sku in skus:
        generate_static_sku_detail_html(sku)
