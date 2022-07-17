# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: auth.py
@Time: 2022/7/1517:17
@Software: PyCharm
"""

import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render


class AuthMiddleware(MiddlewareMixin):
    """
    自定义中间件，用于判断用户是否已经登录
    原理是，django后台处理访问请求，如果不满足中间件定义的判断逻辑
    则请求无法通过中间件，在中间件层直接被返回
    """

    def process_request(self, request):
        """
        处理用户请求，默认返回none相当于穿过当前中间件层，返回值为django返回值类,有返回值时说明请求被阻挡
        :param request:
        :return:
        """
        # 获取uuid,拼接验证码url
        user_uuid = ""
        if request.session.get("uuid"):
            user_uuid = request.session.get("uuid")
        captcha_path = "/captcha/" + user_uuid

        # 验证访问url是否需要登录权限
        user_url = ["/", "/signin/", "/signup/", "/signout/", captcha_path]  # 存放不需要用户登录即可访问的url

        admin_url = ["/teacher/list/", "/teacher/add/", "/teacher/delete/", "/student/delete/"]  # 存放管理员权限访问url
        teacher_pattern = r'(/teacher/edit/[0-9]+)'  # 编辑老师页面url,需要管理员权限,使用正则表达式匹配

        teacher_url = ["/student/list/"]  # 存放教师权限访问url
        student_pattern = r'(/student/edit/[0-9]+)'  # 编辑学生页面url,需要管理员权限,使用正则表达式匹配

        user_pattern = r'/user/reset/(\S+)'  # 重置用户密码,验证是否为当前用户,需要对应的用户id

        path = request.path_info

        # 验证是否已经登录
        if path not in user_url:
            if not request.session.get("userinfo"):
                return redirect("/signin/")

        # 验证是否需要管理员权限
        if (path in admin_url) or re.search(teacher_pattern, path) or re.search(student_pattern, path):
            if request.session.get("userinfo")["identity"] != "管理员":
                return render(request, "error.html", {"msg": "您没有权限,请联系管理员!", "state": "alert-danger"})

        # 验证是否需要教师权限
        if path in teacher_url:
            if request.session.get("userinfo")["identity"] != "管理员" and request.session.get("userinfo")["identity"] != "老师":
                return render(request, "error.html", {"msg": "您没有权限,请联系管理员!", "state": "alert-danger"})

        # 验证是否需要当前用户权限
        if re.search(user_pattern, path):
            if request.session.get("userinfo")["identity"] != "管理员" and request.session.get("userinfo")["name"] != re.search(user_pattern, path).group(1):
                return render(request, "error.html", {"msg": "您没有权限,请联系管理员!", "state": "alert-danger"})

        return
