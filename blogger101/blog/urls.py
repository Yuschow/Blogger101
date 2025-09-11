from django.urls import path
from .views import UserAPI  # 注意这里导入的是类
from .views import GroupAPI
from .views import RoleAPI

urlpatterns = [
    path('user', UserAPI.as_view(), name='user_api'),
    path('group', GroupAPI.as_view(), name='group_api'),
    path('role', RoleAPI.as_view(), name='role_api'),

]
