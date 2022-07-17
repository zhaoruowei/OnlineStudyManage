# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: plugin.py
@Time: 2022/7/1217:14
@Software: PyCharm
"""

import hashlib
from django.conf import settings


def myhash(pwd) -> str:
    """
    sha-256方法对输入的字符串加密处理
    :param pwd:
    :return:
    """
    # 创建加密对象，加盐
    obj = hashlib.sha256(settings.SECRET_KEY.encode('utf-8'))
    obj.update(pwd.encode('utf-8'))
    # 加密
    pwd = obj.hexdigest()
    return pwd
