from django.urls import path

from . import views


urlpatterns = [
    # path('/', views.IndexView.as_view()),
    path('qq/authorization/', views.QQURLView.as_view()),
    # QQ用户部分接口:
    path('oauth_callback/', views.QQUserView.as_view()),
]
