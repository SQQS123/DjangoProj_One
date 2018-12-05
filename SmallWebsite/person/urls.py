from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [

    path('myVIP/', views.myVIP, name='myVIP'),
    path('charge/', views.charge, name='charge'),
    path('myJF/',views.myJF, name='myJF'),
    path('exchange/', views.exchange, name='exchange'),
    path('myFB/', views.myFB, name='myFB'),
    path('notify/',views.notify, name='notify'),

    path('profile/',views.profile, name='profile'),
    path('changepwd/',views.changepwd, name='changepwd'),
    path('resetpwd/', views.resetpwd, name='resetpwd'),
    path('logout/', views.logout, name='logout'),
]