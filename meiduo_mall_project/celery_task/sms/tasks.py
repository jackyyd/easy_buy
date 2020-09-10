"""tasks :固定名称"""
from celery_task.main import celery_app
from celery_task.yuntongxun.sms import CCP


@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile, sms_code):
    """
    ccp发送短信验证码
    :param mobile:
    :param sms_code:
    :return:
    """
    result = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    return result
