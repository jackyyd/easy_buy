import json
import re
from django.utils import timezone
from django.views import View
from django import http
from django.contrib.auth import login, logout, authenticate
from carts.utils import merge_cart_cookie_to_redis
from meiduo_mall_project.utils.views import LoginRequiredJSONMixin
from django.http import JsonResponse
from django.conf import settings
from meiduo_mall_project.settings.dev import logger
from celery_tasks.email.tasks import send_verify_email
from .utils import generate_verify_email_url
from meiduo_mall_project.utils.secret import SecretOauth
from apps.users.models import User
from meiduo_mall_project.utils.logger import logger
from .models import Address
from apps.goods.models import SKU, GoodsVisitCount
from django_redis import get_redis_connection


# 定义用户名类视图
class UsernameCountView(View):
    """
    判断用户名是否重复注册
    """
    def get(self, request, username):
        # 1. 接收参数
        # 2. 校验参数
        # 3. 业务数据处理
        # 3.1 查询username在数据库中的个数
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            settings.logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '访问数据库失败'})
        # 4. 构建响应并返回
        return http.JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


# 定义手机号类视图
class MobileCountView(View):
    """
    判断手机号是否重复注册
    """
    # 1. 获取参数
    def get(self, request, mobile):
        # 异常处理
        try:
            # 判断手机号是否重复（数据处理）
            count = User.objects.filter(mobile = mobile).count()
        except Exception as e:
            return http.JsonResponse({
                'code': 0,
                'errmsg': '查询数据库出错'
            })
        # 构建响应
        return http.JsonResponse({
            'code': 400,
            'errmsg': 'ok',
            'count': count
        })


# 定义用户注册类视图
class RegisterView(View):

    def post(self, request):
        '''接收参数, 保存到数据库'''
         # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())

        # 提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        allow = json_dict.get('allow')
        sms_code = json_dict.get('sms_code')

        # 2.校验(整体参数是否为空)
        if not all([username, password, password2, mobile, sms_code]):
            return http.JsonResponse({'code':400, 'errmsg':'缺少必传参数!'})

        # 3.username检验
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})

        # 4.password检验
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})

        # 5.password2 和 password
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 6.mobile检验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 7.allow检验
        if allow != True:
            return http.JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})


        # 8.注册的核心逻辑-保存到数据库 (username password mobile)
        try:
            user = User.objects.create_user(username=username,
                                             password=password,
                                             mobile=mobile)
        except Exception as e:
            return http.JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        login(request, user)
        # 13.拼接json返回
        # 生成响应对象
        response = http.JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 在响应对象中设置用户名
        # 将用户名写入cookie，有效期14天
        response.set_cookie('username', user.username, max_age=3600*24*14)
        # 返回响应结果
        return merge_cart_cookie_to_redis(request, response)


# 定义用户登录类视图
class LoginView(View):
    """
    实现用户登陆接口
    """
    def post(self, request):
        # 1. 参数接收
        data_dict = json.loads(request.body.decode())
        username = data_dict.get('username')
        password = data_dict.get('password')
        remembered = data_dict.get('remembered')
        # 2. 校验参数
        # 2.1 整体校验
        if not all([username, password]):
            return http.JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })
        # 2.2 部分校验
        # 2.2.1校验用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')
        # 2.2.2检验密码
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        # 3. 业务数据处理
        # 3.1 认证用户
        # 认证用户：使用账号查询用户是否存在，如果用户存在，再检验密码是否正确
        # user = User.objects.get(username=username)
        # user.check_password()
        user = authenticate(request, username=username, password=password)
        if user is None:
            return http.JsonResponse({
                'code': '400',
                'errmsg': '用户名或密码错误'
            })
        # 3.2 设置session
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        # 3.3 状态保持
        login(request, user)
        # 4. 构建响应并返回
        response = http.JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        # 在响应对象中设置用户名信息
        # 将用户名设置在cookie中，有效期14天
        response.set_cookie('username', user.username, max_age=3600*24*14)
        # 返回响应对象# 合并购物车
        return merge_cart_cookie_to_redis(request, response)


# 定义用户退出类视图
class LogoutView(View):
    """
    实现用户退出接口
    """
    def delete(self, request):
        # 清理session
        logout(request)
        # 创建response对象
        response = http.JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 调用delete方法
        response.delete_cookie('username')
        # 返回响应
        return response


# 定义用户中心类视图
class UserInfoView(LoginRequiredJSONMixin, View):
    """
    实现用户中心接口
    """
    def get(self, request):
        """提供个人信息界面"""
        # 获取界面需要数据，进行拼接
        info_data = {
            "username": request.user.username,
            "mobile": request.user.mobile,
            "email": request.user.email
        }
        return http.JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            "info_data": info_data
        })


# 定义邮箱类视图
class EmailView(LoginRequiredJSONMixin, View):
    """
    实现邮箱接口
    """
    def put(self, request):
        # 1. 提取参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')
        # 2. 校验参数
        if not email:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少email参数'
            })
        if not re.match(r'^([a-zA-Z\d])(\w|\-)+@[a-zA-Z\d]+\.[a-zA-Z]{2,4}$',email):
            return JsonResponse({
                'code': 400,
                'errmsg': 'email格式有误'
            })
        # 3. 数据处理
        # 添加邮箱
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            # 记录日志
            settings.logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '添加邮箱失败'
            })
        # 调用函数
        verify_url = generate_verify_email_url(request)
        send_verify_email(email, verify_url)
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


# 定义验证邮箱类视图
class VerifyEmailView(View):
    """
    实现验证邮箱接口
    """
    def put(self, request):
        # 1. 接受参数
        token = request.GET.get('token')
        # 2. 校验参数
        if not token:
            return JsonResponse({'code': 400, 'errmsg': '缺少参数token'})
        # 3. 数据处理
        # 解密
        data_dict = SecretOauth().loads(token)
        # 数据库对比id，email
        try:
            user = User.objects.get(pk=data_dict.get('user_id'), email=data_dict.get('email'))
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '参数有误'})
        try:
            # 修改激活状态
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '激活失败'
            })
        # 4. 构建响应
        return JsonResponse({'code': 0, 'errmsg': '激活成功'})


# 定义新增收货地址类视图
class CreateAddressView(LoginRequiredJSONMixin, View):
    """
    实现新增收货地址接口
    """
    def post(self, request):
        # 1. 接受参数
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')
        # 获取收货地址个数
        count = Address.objects.filter(user=request.user, is_deleted=False).count()
        # 2. 校验参数
        if count >= 20:
            return JsonResponse({
                'code': 400,
                'errmsg': '超过地址数量上限'
            }, status=400)
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            }, status=400)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数mobile有误'
            }, status=400)
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '参数tel有误'
                }, status=400)
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '参数email有误'
                }, status=400)
        # 3. 业务数据处理
        # 3.1 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title=title,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
            # 3.2 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '新增地址失败'
            }, status=400)
            # 将新增的地址响应给前段
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }
        # 4.　构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': '新增地址成功',
            'address': address_dict
        })


# 定义展示收货地址类视图
class AddressView(LoginRequiredJSONMixin, View):
    """实现展示收货地址接口"""
    def get(self, request):
        # 1. 接受参数
        # 2. 校验参数
        # 3. 业务数据处理
        # 3.1 查询所有地址
        try:
            addresses = Address.objects.filter(user=request.user, is_deleted=False)
            # 3.2 遍历
            address_dict_list = []
            for address in addresses:
                address_dict = {
                    'id': address.id,
                    'title': address.title,
                    'receiver': address.receiver,
                    'province': address.province.name,
                    'city': address.city.name,
                    'district': address.district.name,
                    'mobile': address.mobile,
                    'tel': address.tel,
                    'email': address.email
                }
                address_dict_list.append(address_dict)
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '展示收货地址失败'
            }, status=400)
        # 设置默认收货地址
        default_id = request.user.default_address_id
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'addresses': address_dict_list,
            'default_address_id': default_id
        })


# 定义修改和删除收货地址类视图
class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    """实现修改和删除收货地址接口"""
    def put(self, request, address_id):
        """修改收货地址"""
        # 1. 接收参数
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')
        # 2. 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            }, status=400)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数mobile有误'
            }, status=400)
        if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数tel有误'
            }, status=400)
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数email有误'
            }, status=400)
        # 3. 业务数据处理
        try:
            # 3.1 判断地址是否存在，并更新信息
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=request.title,
                receiver=request.receicer,
                province_id=request.province_id,
                city_id=request.city_id,
                district_id=request.district_id,
                place=request.place,
                mobile=request.mobile,
                tel=request.tel,
                email=request.email
            )
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '修改收货地址失败'
            }, status=400)
        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }
        # 4. 构建响应
        return JsonResponse({
            'code': 400,
            'errmsg': 'ok',
            'address': address_dict
        })

    def delete(self, request, address_id):
        """删除收货地址"""
        # 1. 接收参数
        # 2. 校验参数
        # 3. 业务数据处理
        try:
            # 3.1 查询要删除的地址
            address = Address.objects.get(id=address_id)
            # 3.2 将逻辑删除设置位True
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '删除收货地址失败'
            }, status=400)
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


# 定义默认收货地址类视图
class DefaultAddressView(LoginRequiredJSONMixin, View):
    """实现默认收货接口"""
    def put(self, request, address_id):
        # 1. 接收参数
        # 2. 校验参数
        # 3. 业务数据处理
        try:
            # 3.1 接收参数，查询地址
            address = Address.objects.get(id=address_id)
            # 3.2 设置地址为默认地址
            request.user.default_address=address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '设置默认地址失败'
            }, status=400)
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


# 定义修改地址标题类视图
class UpdateAddressTitleView(LoginRequiredJSONMixin, View):
    """实现修改地址标题接口"""
    def put(self, request, address_id):
        # 1. 接收参数
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        # 2. 校验参数
        # 3. 业务数据处理
        try:
            # 3.1 查询地址
            address = Address.objects.get(id=address_id)
            # 3.2 设置新的地址标题
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '修改地址标题失败'
            }, status=400)
        # 4. 构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


# 定义修改密码类视图
class UpdatePasswordView(View):
    """实现修改密码接口"""
    def put(self, request):
        # 1. 接收参数
        json_dict = json.loads(request.body.decode())
        old_password = json_dict.get('old_password')
        new_password = json_dict.get('new_password')
        new_password2 = json_dict.get('new_password2')
        # 2. 校验参数
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            }, status=400)
        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({
                'code': 400,
                'errmsg': '原始密码不正确'
            }, status=400)
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码最少８位，最多２０位'
            }, status=400)
        if new_password != new_password2:
            return JsonResponse({
                'code': 400,
                'errmsg': '两次输入密码不一致'
            }, status=400)
        # 3. 业务数据处理
        try:
            # 3.1 修改密码
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '没有修改密码'
            }, status=400)
        # 3.2 清理状态保持信息
        logout(request)
        # 4. 构建响应
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok',
        })
        response.delete_cookie('username')
        return response


# 用户浏览历史记录
class UserBrowseHistory(LoginRequiredJSONMixin, View):

    def post(self, request):

        user = request.user
        # 1、提取参数
        # 2、校验参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        if not sku_id:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少参数'
            }, status=400)

        try:
            sku = SKU.objects.get(pk=sku_id, is_launched=True)
        except SKU.DoesNotExist as e:
            return JsonResponse({
                'code': 404,
                'errmsg': '商品已下架/不存在'
            }, status=404)

        # 3、数据/业务处理 —— 把访问的sku的id写入redis表示记录一条浏览历史
        # 3.1、获取"history"缓存配置的redis链接
        conn = get_redis_connection('history')
        p = conn.pipeline()
        # 3.2、历史记录写入缓存
        # 3.2.1、去重
        p.lrem(
            'history_%d' % user.id,
            0, # 删除所有指定成员
            sku_id
        )
        # 3.2.2、插入列表头
        p.lpush(
            'history_%d' % user.id,
            sku_id
        )
        # 3.2.3、截断保留5个记录
        p.ltrim(
            'history_%d' % user.id,
            0,
            4
        )
        p.execute()  # 批量执行redis指令

        # TODO: 记录该sku商品的分类访问量
        # 分类id：sku.category_id
        # 当日零时刻：
        cur_0_time = timezone.localtime().replace(hour=0, minute=0, second=0)
        # (1)、判断当前sku商品的分类，和当日的数据存不存在；
        try:
            visit_obj = GoodsVisitCount.objects.get(
                category_id=sku.category_id,
                create_time__gte=cur_0_time
            )
        except GoodsVisitCount.DoesNotExist as e:
            # 记录不存在则新建
            GoodsVisitCount.objects.create(
                category_id=sku.category_id,
                count=1
            )
        else:
            # 记录存在则累加
            visit_obj.count += 1
            visit_obj.save()

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


    # 查看历史
    def get(self, request):
        user = request.user
        # 1、提取参数
        # 2、校验参数
        # 3、数据/业务处理 —— 用户浏览的sku商品信息返回(读redis获取最近浏览的历史sku.id, 读mysql获取sku详细信息)
        # 3.1、读redis获取浏览历史
        conn = get_redis_connection('history')
        # sku_ids = [b'6', b'3', b'4', b'14', b'15']
        sku_ids = conn.lrange(
            'history_%d' % user.id,
            0,
            -1
        )

        skus = []  # 用于记录返回sku商品的详细信息
        # 3.2、读mysql获取详细信息
        for sku_id in sku_ids:
            # sku_id = b'6'
            sku = SKU.objects.get(pk=int(sku_id))
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image_url.url,
                'price': sku.price
            })

        # 4、构建响应
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'skus': skus
        })
