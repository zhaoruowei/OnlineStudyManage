# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Ruowei Zhao
@Student number: 210464838
@Email: r.zhao@se21.qmul.ac.uk
@Project: OnlineStudyManage
@File: pagination.py
@Time: 2022/7/173:28
@Software: PyCharm
"""

from django.utils.safestring import mark_safe


class Pagination:
    """
    分页显示组件
    在views中:
        def pretty_list(request):
            # 筛选数据
            queryset = PrettyNum.objects.all() # 获取所有数据库记录
            # 实例化分页对象
            page_obj = Pagination(request, queryset)
            # 获取分页后的内容返回前端
            context = {
                "queryset": page_obj.page_queryset, # 分完页后的数据库对象
                "page_string": page_obj.html() # 生成页码前端HTML标签
            }
            return render(request, "pretty_list.html", context)

    在HTML模板中:
        {% for obj in queryset %}
            {{ obj.xx }}
        {% endfor %}

        <nav aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
                {{ page_html }}
            </ul>
        </nav>
    """

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=2):
        """

        :param request: 请求对象
        :param queryset: 查询数据库得到的查询对象
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数,例如/pretty/list/?page=12,表明显示第12页
        :param plus:显示当前页数的前后显示页数范围,默认为2,即当前页面为3时共显示按钮1,2,3,4,5
        """
        # 获取GET请求传递的参数,表示需要显示的页数,默认显示第1页
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page  # 当前页面
        self.page_size = page_size  # 每页显示的数据库对象数
        self.start = (page - 1) + page_size  # 起始显示数据库对象
        self.end = page * page_size  # 结束显示数据库对象
        self.queryset = queryset  # 获取查询到的所有数据库对象
        self.plus = plus
        self.total_page_count = self.total_page()

    def total_page(self):
        """ 根据查询到的总条数和每页显示条数计算一共需要多少页 """
        total_count = self.queryset.count()  # 统计一共多少条记录被查询到
        # 计算一共需要多少页显示
        # 使用总条数除以每页显示的条数,得到商为一共需要的页数-1,余数为不满1页的结果条数
        total_page_count, div = divmod(total_count,
                                       self.page_size)  # python 内置函数divmod(x, y),结果位x/y的元组结果，元组元素1为商，元素2为余数
        if div:  # 余数不为0,总页码加1
            total_page_count += 1
        return total_page_count

    def html(self):
        """
        使用 from django.utils.safestring import mark_safe
        中的mark_safe函数将str转换为html标签,返回前端,显示页码控件
        :return:
        """
        # 存放页码html list
        page_str_list = []
        # 生成前一页标签,当前页小于1时,上一页按钮不能使用
        if self.page > 1:
            elem = "<li class='page-item'>" \
                   "<a class='page-link' href='?page={}' aria-label='Previous'>" \
                   "<span aria-hidden='true'>&laquo;</span></a></li>".format(self.page - 1)
            page_str_list.append(elem)
        else:
            elem = "<li class='page-item disabled'>" \
                   "<a class='page-link' href='' aria-label='Previous'>" \
                   "<span aria-hidden='true'>&laquo;</span></a></li>"
            page_str_list.append(elem)
        # 根据当前页面显示的页码范围生成每一个页码标签
        for i in range(self.start - 1, self.end):
            if self.page == i + 1:
                elem = "<li class='page-item active'><a class='page-link' href='?page={}'>{}</a></li>".format(i + 1,
                                                                                                              i + 1)  # 通过get请求传递参数
            else:
                elem = "<li class='page-item'><a class='page-link' href='?page={}'>{}</a></li>".format(i + 1,
                                                                                                       i + 1)  # 通过get请求传递参数
            page_str_list.append(elem)

        # 生成后一页标签,当前页等于最大页时,下一页按钮不能使用
        if self.page != self.total_page_count:
            elem = "<li class='page-item'>" \
                   "<a class='page-link' href='?page={}' aria-label='Previous'>" \
                   "<span aria-hidden='true'>&raquo;</span></a></li>".format(self.page + 1)
            page_str_list.append(elem)
        else:
            elem = "<li class='page-item disabled'>" \
                   "<a class='page-link' href='' aria-label='Previous'>" \
                   "<span aria-hidden='true'>&raquo;</span></a></li>"
            page_str_list.append(elem)

        page_string = mark_safe("".join(page_str_list))  # 将str转换为html标签

        return page_string

    def page_queryset(self):
        """
        获取每页显示的数据库对象
        :return:
        """
        # 计算出显示的页码范围
        if self.total_page_count <= 2 * self.plus + 1:
            self.start = 1
            self.end = self.total_page_count
        else:
            if self.page <= self.plus:
                self.start = 1
                self.end = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    self.start = self.total_page_count - 2 * self.plus
                    self.end = self.total_page_count
                else:
                    self.start = self.page - self.plus
                    self.end = self.page + self.plus

        # 计算每页起始的数据和结束的数据
        if self.page == 1:
            start = 0
            end = self.page_size + 1
        else:
            start = self.page_size * (self.page - 1) + 1
            end = start + self.page_size

        return self.queryset[start:end]
