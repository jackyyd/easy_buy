from django import http
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """
    自定义LoginRequiredMixin
    """
    def handle_no_permission(self):
        return http.JsonResponse({'code': 400, 'errmsg': '用户未登录'}, status=401)
