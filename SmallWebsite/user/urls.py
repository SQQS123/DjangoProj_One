from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [

    #也可以使用django内置的用户来搞
    # path('logintest/',auth_views.LoginView.as_view(template_name='inner_login.html'), name='logintest'),

    # 用户注册
    path('register/',views.u_register, name='register'),
    path('register/',views.u_register, name='registertest'),

    # 用户登录
    path('login/',views.u_login, name='logintest'),
    path('login/',views.u_login, name='login'),

    # 忘记密码
    path('forget/',views.u_forget, name='forget'),

    # 重置密码
    path('reset/',views.u_reset, name='reset'),
]