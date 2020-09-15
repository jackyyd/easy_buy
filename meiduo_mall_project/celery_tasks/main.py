"""
定义异步应用对象
"""
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall_project.settings.dev')


# 定义一个异步应用对象
celery_app = Celery('meiduo')
# 配置美多对象
celery_app.config_from_object('celery_tasks.config')
# 自动捕获tasks
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
