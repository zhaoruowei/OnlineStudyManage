# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: plugins.py
@Time: 2022/6/230:09
@Software: PyCharm
"""

import random

from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def get_captcha(width=150, height=50, font_size=35, captcha_length=5, font_type="Monaco.ttf"):
    """ 生成图片验证码 """

    def random_color():
        """
        生成随机RGB颜色
        :return:三个0-255范围的整数的元组
        """
        return (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

    def random_char():
        """
        生成随机字符
        :return:随机大小写字母（ascii65-90）
        """
        return chr(random.randint(65, 91))

    # 生成随机背景色
    bg_color = random_color()
    # 调用pillow，生成图片
    image = Image.new(mode="RGB", size=(width, height), color=bg_color)
    draw = ImageDraw.Draw(image, mode="RGB")
    image_font = ImageFont.truetype(font=font_type, size=font_size)
    code = ""
    # 画随机字母
    for i in range(captcha_length):
        # 随机生成字母坐标
        x = i * (width / captcha_length)
        y = random.randint(0, height - font_size)
        # 随机生成字母颜色
        color = random_color()
        # 随机生成验证码
        char = random_char()
        code += char
        draw.text((x, y), char, fill=color, font=image_font)

    # 画干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=random_color())

    # 画干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return image, code


def captcha_validation(user_uuid, code):
    """
    验证码验证函数
    :param user_uuid: 用户从服务器获取的uuid值
    :param code: 用户从前端页面提交的验证码
    :return: 如果根据uuid获取缓存中保存的验证码与用户提交的验证码不一致，返回字符串“验证码错误”
    如果用户没有提交验证码，返回字符串“验证码为空”
    如果验证通过，返回空
    分装前
    # captcha_code = request.POST.get("captcha_code").upper()
    # if not captcha_code:
    #     return render(request, "signin.html", {'form': form, 'captcha_error': '验证码为空！', 'uuid': user_uuid})
    # elif cache.get(user_uuid) != captcha_code:
    #     return render(request, "signin.html", {'form': form, 'captcha_error': '验证码错误！', 'uuid': user_uuid})
    """
    if not code:
        return "验证码为空！"
    elif code != cache.get(user_uuid):
        return "验证码错误！"
