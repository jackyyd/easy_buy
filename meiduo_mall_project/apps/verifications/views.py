from django.views import View
from django import http
from django_redis import get_redis_connection
from apps.verifications.libs.captcha.captcha import captcha
import random
from verifications.libs.yuntongxun.sms import CCP
from meiduo_mall_project.settings.dev import logger
from celery_task.sms.tasks import ccp_send_sms_code


# 定义图形验证码类视图
class ImageCodeView(View):
    """图形验证码
    GET http://www.meiduo.site:8000/image_codes/550e8400-e29b-41d4-a716-446655440000/
    """

    def get(self, request, uuid):
        """
        实现图形验证码逻辑
        :param uuid: UUID
        :return: image/jpg
        """
        # 生成图形验证码
        text, image = captcha.generate_captcha()

        # 保存图形验证码
        # 使用配置的redis数据库的别名，创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 使用连接到redis的对象去操作数据存储到redis
        # redis_conn.set('key', 'value') # 因为没有有效期
        # 图形验证码必须要有有效期的：美多商城的设计是300秒有效期
        # redis_conn.setex('key', '过期时间', 'value')
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 响应图形验证码: image/jpg
        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 1. 接收参数
        image_code_client = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('image_code_id')

        # 2. 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': 400,
                                      'errmsg': '缺少必传参数'})

        # 3. 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')

        # 4. 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': 400,
                                      'errmsg': '图形验证码失效'})

        # 5. 删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 6. 对比图形验证码
        # bytes 转字符串
        image_code_server = image_code_server.decode()
        # 转小写后比较
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse({'code': 400,
                                      'errmsg': '输入图形验证码有误'})

        # 7. 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 8. 保存短信验证码
        # 短信验证码有效期，单位：300秒
        redis_conn.setex('sms_%s' % mobile,
                         300,
                         sms_code)

        # 9. 发送短信验证码
        # 短信模板
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        print('短信验证码:', sms_code)
        # # 9. 异步发送验证码
        # ccp_send_sms_code.delay(mobile, sms_code)

        # 10. 响应结果
        return http.JsonResponse({'code': 0,
                                  'errmsg': '发送短信成功'
                                  })
