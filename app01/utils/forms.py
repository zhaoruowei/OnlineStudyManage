# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: forms.py
@Time: 2022/6/2221:12
@Software: PyCharm
"""

from django import forms
from django.core.validators import ValidationError

from app01.utils.bootstrap import UserBootstrapModelForm
from app01.models import User, Teacher, Student
from app01.utils.plugin import myhash


class SigninForm(UserBootstrapModelForm):
    # User model中定义的username字段有独一性要求，在使用is_valid验证时也会验证是否唯一
    # 由于在登陆时不需要验证是否唯一所以自定义字段name，从而跳过唯一性验证，获得的clean_data保存到username字段
    name = forms.CharField(label="用户名")

    class Meta:
        model = User
        fields = ["name", "password"]
        widgets = {
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        # 密码进行hash处理，与数据库比对
        pwd = self.cleaned_data.get("password")
        return myhash(pwd)


class SignupForm(UserBootstrapModelForm):
    confirmpassword = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "confirmpassword"]
        widgets = {
            "password": forms.PasswordInput,
        }

    # 钩子函数验证密码与确认密码
    def clean_confirmpassword(self):
        pwd = self.cleaned_data.get("password")
        confirm = myhash(self.cleaned_data.get("confirmpassword"))
        if confirm != pwd:
            raise ValidationError("密码不一致！")

    # 对密码进行加密处理
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return myhash(pwd)


class UserResetForm(UserBootstrapModelForm):
    confirmpassword = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["password", "confirmpassword"]
        widgets = {
            "password": forms.PasswordInput,
        }

    # 钩子函数验证密码与确认密码
    def clean_confirmpassword(self):
        pwd = self.cleaned_data.get("password")
        confirm = myhash(self.cleaned_data.get("confirmpassword"))
        if confirm != pwd:
            raise ValidationError("密码不一致！")

    # 对密码进行加密处理
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return myhash(pwd)


class TeacherForm(UserBootstrapModelForm):
    user_name = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ["user_name", "password", "confirmpassword", "name", "gender", "email", "phone", "salary", "classes",
                  "join_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置时间INPUT框属性
        for name, field in self.fields.items():
            if name == "join_time":
                field.widget.attrs = {
                    "id": "datepicker1",
                    "type": "text",
                    "class": "form-control datepicker_input border-2",
                    "placeholder": "YYYY/MM/DD",
                }

    # 对密码进行加密处理
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return myhash(pwd)

    # 钩子函数验证密码与确认密码
    def clean_confirmpassword(self):
        pwd = self.cleaned_data.get("password")
        confirm = myhash(self.cleaned_data.get("confirmpassword"))
        if confirm != pwd:
            raise ValidationError("密码不一致！")

    # 钩子函数验证用户名是否存在
    def clean_user_name(self):
        user_name = self.cleaned_data.get("user_name")
        if User.objects.filter(username=user_name).exists():
            raise ValidationError("用户名已存在！")
        return user_name


class TeacherEditForm(UserBootstrapModelForm):
    class Meta:
        model = Teacher
        exclude = ["username"]


class StudentForm(UserBootstrapModelForm):
    user_name = forms.CharField(label="用户名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ["user_name", "password", "confirmpassword", "name", "gender", "email", "phone", "classes",
                  "join_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置时间INPUT框属性
        for name, field in self.fields.items():
            if name == "join_time":
                field.widget.attrs = {
                    "id": "datepicker1",
                    "type": "text",
                    "class": "form-control datepicker_input border-2",
                    "placeholder": "YYYY/MM/DD",
                }

    # 对密码进行加密处理
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return myhash(pwd)

    # 钩子函数验证密码与确认密码
    def clean_confirmpassword(self):
        pwd = self.cleaned_data.get("password")
        confirm = myhash(self.cleaned_data.get("confirmpassword"))
        if confirm != pwd:
            raise ValidationError("密码不一致！")

    # 钩子函数验证用户名是否存在
    def clean_user_name(self):
        user_name = self.cleaned_data.get("user_name")
        if User.objects.filter(username=user_name).exists():
            raise ValidationError("用户名已存在！")
        return user_name


class StudentEditForm(UserBootstrapModelForm):
    class Meta:
        model = Student
        exclude = ["username"]
