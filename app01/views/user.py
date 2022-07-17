# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: user.py
@Time: 2022/6/2214:31
@Software: PyCharm
"""

import uuid
from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.core.cache import cache

from app01.models import User
from app01.utils.forms import SigninForm, SignupForm, UserResetForm
from app01.utils.captcha import get_captcha, captcha_validation


def captcha(request, id):
    """
    生成随机验证码
    通过动态url获取传递的uuid值
    调用验证码生成函数，生成随机验证码和验证码图片
    将图片存入系统内存中，将验证码存入django文件缓存中（可替换成其他缓存系统，图片的缓存也可以优化）
    设置缓存有效期和cookie中的uuid有效期一致为60s，即cookie中的uuid对应生成的验证码
    :param request:
    :param id:
    :return:
    """
    # 将图片保存到内存
    stream = BytesIO()
    img, code = get_captcha()
    img.save(stream, 'png')
    # 将验证码保存到缓存中,对应每次登录生成的uuid,60s过期
    cache.set(id, code, 60)
    return HttpResponse(stream.getvalue(), content_type='image/png')


def sign_in(request):
    """
    用户登录
    接收请求时，生成随机uuid，存入cookie，设置有效期60s，将uuid通过模板返回前端页面
    POST请求时，通过modelform获取表单用户名，密码字段并进行验证。
    通过post.get获取表单验证码字段，获取cookie中的uuid，根据uuid查询存储在缓存中对应的验证码，进行验证码验证
    验证完成，表示登陆成功，设置cookie
    验证失败，返回前端相关错误信息
    :param request:
    :return:
    """
    # 生成uuid
    if request.session.get("uuid") is None:
        user_uuid = str(uuid.uuid4())
        request.session["uuid"] = user_uuid
        request.session.set_expiry(60)
    user_uuid = request.session.get("uuid")

    # 处理GET请求
    if request.method == "GET":
        form = SigninForm()
        return render(request, "signin.html", {'form': form, 'uuid': user_uuid})

    # 生成表单
    form = SigninForm(data=request.POST)

    # 验证码验证
    captcha_error = captcha_validation(user_uuid, request.POST.get("captcha_code").upper())
    if captcha_error:
        return render(request, "signin.html", {'form': form, 'captcha_error': captcha_error, "uuid": user_uuid})

    # 表单验证
    if form.is_valid():
        # 查询数据库
        user_object = User.objects.filter(username=form.cleaned_data["name"],
                                          password=form.cleaned_data["password"]).first()

        if not user_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "signin.html", {'form': form, 'uuid': user_uuid})

        # 验证通过，登陆成功，设置cookie
        # 清除captcha uuid
        request.session.pop("uuid")
        request.session["userinfo"] = {"id": user_object.id, "name": user_object.username,
                                       "identity": user_object.get_identity_display()}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/")
    return render(request, "signin.html", {'form': form, 'uuid': user_uuid})


def sign_up(request):
    """ 用户注册 """
    # 生成uuid获取验证码
    if request.session.get("uuid") is None:
        user_uuid = str(uuid.uuid4())
        request.session["uuid"] = user_uuid
        request.session.set_expiry(60)
    user_uuid = request.session.get("uuid")

    if request.method == "GET":
        form = SignupForm()
        return render(request, "signup.html", {'form': form, 'uuid': user_uuid})

    # 获取表单
    form = SignupForm(data=request.POST)

    # 验证码验证
    captcha_error = captcha_validation(user_uuid, request.POST.get("captcha_code").upper())
    if captcha_error:
        return render(request, "signup.html", {'form': form, 'captcha_error': captcha_error, "uuid": user_uuid})

    # 表单验证
    if form.is_valid():
        form.save()
        return redirect(to="/signin/")

    return render(request, "signup.html", {'form': form, "uuid": user_uuid})


def sign_out(request):
    """
    注销，清除当前用户session
    :param request:
    :return:
    """
    # clear删除session中的value， flush删除整条cookie
    # request.session.clear()
    request.session.flush()
    return redirect("/")


def user_reset(request, user_name):
    """ 重置用户密码 """
    obj = User.objects.filter(username=user_name).first()
    if not obj:
        return render(request, "error.html", {"msg": "用户不存在!", "state": "alert-danger"})

    if request.method == "GET":
        form = UserResetForm()
        return render(request, "reset.html", {"form": form})

    form = UserResetForm(data=request.POST, instance=obj)

    if form.is_valid():
        form.save()
        return render(request, "error.html", {"msg": "重置成功!", "state": "alert-success"})

    return render(request, "reset.html", {"form": form})
