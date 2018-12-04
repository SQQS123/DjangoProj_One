from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('',views.test,name='test'),
    path('fb/', views.fb,name='fb'),
    path('detail/<kind>/<int:article_id>', views.showdetail, name='detail'),
]