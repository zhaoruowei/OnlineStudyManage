# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: index.py
@Time: 2022/6/2123:54
@Software: PyCharm
"""

from django.shortcuts import render


def index(request):
    return render(request, "index.html")
