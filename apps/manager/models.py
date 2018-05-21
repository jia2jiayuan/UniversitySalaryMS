from django.db import models
# django内置用户基础表
from django.contrib.auth.models import AbstractUser
# 时间模块，用于添加时间信息
from datetime import datetime


class Manager(AbstractUser):
    """
    管理者信息表，扩展了django默认用户表
    还需要在setting中配置 AUTH_USER_MODEL = 'manager.Manager' 替换掉默认User表
    """
    SEX = (
        ('male', '男'),
        ('female', '女')
    )
    IS_STATUS = (
        (0, '不是'),
        (1, '是')
    )
    name = models.CharField(max_length=20, verbose_name="姓名")
    image = models.ImageField(max_length=50, upload_to="manager/%Y/%m", null=True, blank=True, verbose_name="照片")
    sex = models.CharField(max_length=6, choices=SEX,default="male", verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    phone_number = models.CharField(max_length=11, verbose_name='手机号码')
    qq_number = models.CharField(max_length=11, verbose_name='QQ账号')
    work_description = models.TextField(null=True, blank=True, verbose_name="职业描叙")
    # work_description = UEditorField(verbose_name="职业描叙", imagePath='manager/images/%Y/%m', width=1000,
    #                          height=300, filePath='manager/files/%Y/%m', null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, verbose_name="登录账号")
    is_superuser = models.IntegerField(choices=IS_STATUS,default=0, verbose_name="是否超级用户")
    is_staff = models.IntegerField(choices=IS_STATUS,default=0, verbose_name="管理员")
    is_active = models.IntegerField(choices=IS_STATUS,default=0, verbose_name="是否激活账号")
    join_time = models.DateTimeField(default=datetime.now, verbose_name="入职时间")

    # 去除django中默认user表中不需要的字段
    date_joined = None
    first_name = None
    last_name = None

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加记录时间")

    class Meta:
        """
        后台显示表别名
        """
        verbose_name = "管理员信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 创建对象返回的信息提示
        return self.name

    def worklog_num(self):
        return self.worklog_set.all().count()
    worklog_num.short_description = "日志数量"



class Worklog(models.Model):
    """
    管理员工作日志记录表
    """
    WORK_STATUS = (
        (0, "未完成"),
        (1, "完成"),
    )
    name = models.CharField(max_length=20, verbose_name="工作名")
    content = models.TextField(null=True, blank=True, verbose_name="工作内容")
    # content = UEditorField(verbose_name="工作内容", imagePath='worklog/images/%Y/%m', width=1000,
    #                          height=300, filePath='worklog/files/%Y/%m', null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    has_finished = models.IntegerField(choices=WORK_STATUS, default=0, verbose_name="是否完成工作")
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="管理员")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加记录时间")

    class Meta:
        verbose_name = "工作日志信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name