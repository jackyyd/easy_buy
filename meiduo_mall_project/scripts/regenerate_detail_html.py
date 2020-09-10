# 指定Python脚本解析器
#!/usr/bin/env python
# 添加Python脚本导包路径
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from apps.contents.crons import *
# 加载django程序的环境
# 设置django运行所需要的环境
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MOUDLE'] = 'meiduo_mall_project.settings.dev'
# django初始化
import django
django.setup()
from apps.contents.crons import get_categories
from apps.goods.utils import get_breadcrumb, get_goods_and_spec
from apps.goods.models import SKU
from django.template import loader
from django.conf import settings


def generate_static_sku_detail_html(sku_id):
    """
    生成指定sku商品的详情页面
    :param sku_id:
    :return:
    """
    # 查询商品频道分类
    categories = get_categories()
    # 查询面包屑导航
    breadcrumb = get_breadcrumb(sku.category)
    # 查询当前商品规格
    goods_specs = get_goods_and_spec(sku_id)
    # 1. 获得模板
    template = loader.get_template('detail.html')
    # 2. 设置参数
    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'goods_specs': goods_specs
    }
    # 3. 渲染页面
    detail_html_str = template.render(context)
    # 4. 写入文件
    file_path = os.path.join(os.path.dirname(os.path.dirname(settings.STATIC_FILE_PATH)),
                             'front_end_pc/goods'+str(sku_id)+'.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(detail_html_str)


if __name__ == '__main__':
    # 脚本入口：查询所有的sku信息，遍历他们，每遍历一个sku就生成一个对应的详情页
    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku)
