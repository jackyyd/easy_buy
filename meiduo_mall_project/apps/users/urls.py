from django.urls import path,re_path
from . import views


urlpatterns = [
    # 用户名是否重复
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', views.MobileCountView.as_view()),
    re_path('register/', views.RegisterView.as_view())
]
