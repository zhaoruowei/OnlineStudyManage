# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: teacher.py
@Time: 2022/6/2122:41
@Software: PyCharm
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse

from app01.utils.forms import TeacherForm, TeacherEditForm
from app01.models import Teacher, User
from app01.utils.pagination import Pagination


def teacher_list(request):
    """ 查询教师数据库，显示教师信息，需要管理员权限 """
    queryset = Teacher.objects.all()  # 获取所有数据库记录
    # 实例化分页对象
    page_obj = Pagination(request, queryset)
    content = {
        "queryset": page_obj.page_queryset(),
        "page_html": page_obj.html(),
    }
    return render(request, "teacher_list.html", content)


def teacher_add(request):
    """ 创建教师账号以及信息，数据写入user与teacher表中，需要管理员权限 """
    if request.method == "GET":
        form = TeacherForm()
        return render(request, "teacher_add.html", {"form": form})

    form = TeacherForm(data=request.POST)

    # 表单验证
    if form.is_valid():
        User.objects.create(username=form.cleaned_data.get("user_name"), password=form.cleaned_data.get("password"),
                            identity=2)
        data_dic = form.cleaned_data
        data_dic.setdefault("username", User.objects.filter(username=data_dic["user_name"]).first())
        data_dic.pop("user_name")
        data_dic.pop("password")
        data_dic.pop("confirmpassword")
        Teacher.objects.create(**data_dic)
        return redirect("/teacher/list/")

    return render(request, "teacher_add.html", {"form": form})


def teacher_edit(request, nid):
    """ 编辑教师信息,数据写入user与teacher表中，需要管理员权限 """
    # 根据传递的id,获取修改对象
    obj = Teacher.objects.filter(id=nid).first()
    if not obj:
        return render(request, "error.html", {"msg": "用户不存在!", "state": "alert-danger"})
    if request.method == "GET":
        form = TeacherEditForm(instance=obj)
        return render(request, "teacher_edit.html", {"form": form})

    form = TeacherEditForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()

    return render(request, "error.html", {"msg": "修改成功!", "state": "alert-success"})


def teacher_delete(request):
    """ 删除教师信息,级联删除user,teacher表中数据 """
    user_name = request.GET.get("user_name")
    User.objects.filter(username=user_name).delete()
    return JsonResponse({"code": 204})
