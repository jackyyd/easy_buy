from django.template import loader
from apps.goods.models import GoodsChannel
from apps.contents.models import ContentCategory, Content
from django.conf import settings
import os


def get_categories():
    """
    商品分类
    :return:
    """
    categories = {} # # 商品分类频道

    # 按照组id排序，再按照sequence排序
    channels = GoodsChannel.objects.order_by(
        'group_id',
        'sequence'
    )

    # 遍历每一个频道。把频道插入以"组id"为键的键值对中
    for channel in channels:
        # 当前组不存在的时候(第一次构建)
        if channel.group_id not in categories:
            # categories[1] = {}
            categories[channel.group_id] = {
                'channels': [], # 一级分类信息
                'sub_cats': [] # 二级分类
            }
        # 一级分类
        cat1 = channel.category
        categories[channel.group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        # 二级分类
        cat2s = cat1.subs.all()
        for cat2 in cat2s:
            # cat2：每一个二级分类对象

            # 当前二级分类关联的三级分类
            cat3s_list = []
            cat3s = cat2.subs.all()
            for cat3 in cat3s:
                # cat3：当前二级分类关联的每一个三级分类对象
                cat3s_list.append({
                    'id': cat3.id,
                    'name': cat3.name
                })

            categories[channel.group_id]['sub_cats'].append({
                'id': cat2.id,
                'name': cat2.name,
                'sub_cats': cat3s_list # 三级分类
            })
    return categories


def get_contents():
    """
    广告内容
    :return:

    """
    contents = {}
    # 所有广告分类
    content_cats = ContentCategory.objects.all()
    for content_cat in content_cats:
        # content_cat: 每一个分类如：轮播图
        # 当前广告分类关联的所有广告加入列表中
        # contents['index_lbt'] = [<美图M8s>, <黑色星期五>...]
        contents[content_cat.key] = Content.objects.filter(
            category=content_cat,
            status=True  # 正在展示的广告
        ).order_by('sequence')
    return contents


def generate_static_index_html():
    """
    渲染完整首页index.html
    :return:
    """
    # 1. 获取首页数据
    # 1.1 获取商品分类数据
    categories = get_categories()
    # 1.2 获取广告内容数据
    contents = get_contents()
    # 2 获取模板
    # 2.1 获取模板对象
    template = loader.get_template('index.html')
    # 3. 往模板里填入参数
    context = {
        'categories': categories,  # 商品分类
        'contents': contents  # 广告内容
    }
    # 3. 渲染模板
    page = template.render(context)
    path = os.path.join(settings.STATIC_FILE_PATH, 'index.html')
    # 4. 写入静态文件
    with open(path, 'w') as f:
        f.write(page)
