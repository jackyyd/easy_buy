import os
from django.conf import settings
from django.template import loader
from apps.goods.utils import get_goods_and_spec, get_categories
from celery_tasks.main import celery_app


@celery_app.task(name='generate_static_sku_detail_html')
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
