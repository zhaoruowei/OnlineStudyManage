from django.db import models


# Create your models here.
class User(models.Model):
    """ 用户信息 """
    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    identity_choices = (
        (1, "管理员"),
        (2, "老师"),
        (3, "学生"),
    )
    identity = models.SmallIntegerField(verbose_name="用户身份", choices=identity_choices, default=3)
    avatar = models.ImageField(verbose_name="头像", max_length=128, upload_to="avatar/", null=True, blank=True,
                               default="NULL")
    create_time = models.DateField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    """ 老师信息 """
    username = models.ForeignKey(to="User", to_field="username", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=32)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    phone = models.CharField(verbose_name="手机号码", max_length=11, null=True, blank=True)
    salary = models.DecimalField(verbose_name="月薪", max_digits=10, decimal_places=2, null=True, blank=True)
    classes = models.ForeignKey(verbose_name="班级", to="Classes", to_field="class_id", on_delete=models.SET(0), default=0)
    join_time = models.DateField(verbose_name="入职时间")
    leave_time = models.DateField(verbose_name="离职时间", null=True, blank=True)


class Classes(models.Model):
    """ 班级信息 """
    class_id = models.SmallIntegerField(verbose_name="班号", unique=True)
    class_choices = (
        (1, "古筝"),
        (2, "国画"),
    )
    class_type = models.SmallIntegerField(verbose_name="课程类型", choices=class_choices)

    def __str__(self):
        return str(self.class_id)


class Student(models.Model):
    """ 学生信息 """
    username = models.ForeignKey(to="User", to_field="username", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=32)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    phone = models.CharField(verbose_name="手机号码", max_length=11, null=True, blank=True)
    classes = models.ForeignKey(verbose_name="班级", to="Classes", to_field="class_id", on_delete=models.SET(0), default=0)
    join_time = models.DateField(verbose_name="入学时间")
    leave_time = models.DateField(verbose_name="结束时间", null=True, blank=True)


class order(models.Model):
    """ 订单信息 """
    create_time = models.DateField(verbose_name="创建时间", auto_now_add=True)
