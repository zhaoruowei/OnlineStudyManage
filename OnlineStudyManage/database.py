# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: database.py
@Time: 2022/6/2117:36
@Software: PyCharm
"""

import os

from django.conf import settings

engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'mysql': 'django.db.backends.mysql',
}


def config():
    """ 部署在OpenShift上时，用于保密 """
    if settings.DEBUG:  # 如果开启DEBUG模式，即开发模式，使用本地配置
        return {
            'ENGINE': engines['mysql'],
            'NAME': "OnlineStudyManage",
            'USER': "root",
            'PASSWORD': "root123",
            'HOST': "127.0.0.1",
            'PORT': 3306,
        }
    else:
        service_name = os.getenv('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
        if service_name:
            engine = engines.get(os.getenv('DATABASE_ENGINE'), engines['mysql'])
        else:
            engine = engines['sqlite']
        name = os.getenv('DATABASE_NAME')
        if not name and engine == engines['sqlite']:
            name = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        return {
            'ENGINE': engine,
            'NAME': name,
            'USER': os.getenv('DATABASE_USER'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD'),
            'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name)),
            'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name)),
        }
    pass
