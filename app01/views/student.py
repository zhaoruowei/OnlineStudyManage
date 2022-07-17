# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: student.py
@Time: 2022/7/175:33
@Software: PyCharm
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse

from app01.utils.forms import StudentForm, StudentEditForm
from app01.models import User, Student
from app01.utils.pagination import Pagination


def student_list(request):
    """ 查询学生数据库，显示学生信息，需要管理员或教师权限 """
    queryset = Student.objects.all()  # 获取所有数据库记录
    # 实例化分页对象
    page_obj = Pagination(request, queryset)
    content = {
        "queryset": page_obj.page_queryset(),
        "page_html": page_obj.html(),
    }
    return render(request, "student_list.html", content)


def student_add(request):
    """ 创建学生账号以及信息，数据写入user与student表中，需要管理员权限 """
    if request.method == "GET":
        form = StudentForm()
        return render(request, "student_add.html", {"form": form})

    form = StudentForm(data=request.POST)

    # 表单验证
    if form.is_valid():
        User.objects.create(username=form.cleaned_data.get("user_name"), password=form.cleaned_data.get("password"),
                            identity=3)
        data_dic = form.cleaned_data
        data_dic.setdefault("username", User.objects.filter(username=data_dic["user_name"]).first())
        data_dic.pop("user_name")
        data_dic.pop("password")
        data_dic.pop("confirmpassword")
        Student.objects.create(**data_dic)
        return redirect("/student/list/")

    return render(request, "student_add.html", {"form": form})


def student_edit(request, nid):
    """ 编辑学生信息,数据写入user与student表中，需要管理员权限 """
    # 根据传递的id,获取修改对象
    obj = Student.objects.filter(id=nid).first()
    if not obj:
        return render(request, "error.html", {"msg": "用户不存在!", "state": "alert-danger"})
    if request.method == "GET":
        form = StudentEditForm(instance=obj)
        return render(request, "student_edit.html", {"form": form})

    form = StudentEditForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()

    return render(request, "error.html", {"msg": "修改成功!", "state": "alert-success"})


def student_delete(request):
    """ 删除教师信息,级联删除user,teacher表中数据 """
    user_name = request.GET.get("user_name")
    Student.objects.filter(username=user_name).delete()
    return JsonResponse({"code": 204})
