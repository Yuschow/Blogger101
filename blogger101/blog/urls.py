from django.urls import path
from .views import UserAPI  # 注意这里导入的是类

urlpatterns = [
    path('user', UserAPI.as_view(), name='user_api'),
]
