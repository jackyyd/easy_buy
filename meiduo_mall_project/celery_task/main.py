"""
定义异步应用对象
"""
from celery import Celery


# 定义一个异步应用对象
celery_app = Celery('meiduo')
# 配置美多对象
celery_app.config_from_object('celery_task.config')
# 自动捕获tasks
celery_app.autodiscover_tasks(['celery_task.sms'])