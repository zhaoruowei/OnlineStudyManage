"""OnlineStudyManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from app01.views import teacher, index, user, student

urlpatterns = [
    # 设置media文件夹访问路由
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 首页
    path('', index.index),

    # 用户模块
    # 登录
    path('signin/', user.sign_in),
    # 注册
    path('signup/', user.sign_up),
    # 注销
    path('signout/', user.sign_out),
    # 生成验证码图片
    path('captcha/<uuid:id>', user.captcha),
    # 重置用户密码
    path('user/reset/<str:user_name>', user.user_reset),

    # 老师管理，管理员权限
    # 查看所有老师
    path('teacher/list/', teacher.teacher_list),
    # 添加老师
    path('teacher/add/', teacher.teacher_add),
    # 编辑老师
    path('teacher/edit/<int:nid>', teacher.teacher_edit),
    # 删除老师
    path('teacher/delete/', teacher.teacher_delete),

    # 学生管理
    # 查看所有学生,管理员或教师权限
    path('student/list/', student.student_list),
    # 添加老师
    path('student/add/', student.student_add),
    # 编辑学生,管理员权限
    path('student/edit/<int:nid>', student.student_edit),
    # 删除学生,管理员权限
    path('student/delete/', student.student_delete),


]
