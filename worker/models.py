from django.db import models
from datetime import  datetime


class Job(models.Model):
    """
    职位信息表
    """
    IS_CORE = (
        (0, '不是'),
        (1, '是')
    )
    name = models.CharField(max_length=20, verbose_name="职位名")
    description = models.TextField(verbose_name="工作描叙")
    expect_salary = models.DecimalField(verbose_name="预估工资")
    is_core = models.IntegerField(choices=IS_CORE, default=0, verbose_name="是否是核心职位")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加记录时间")

    class Meta:
        verbose_name = "职位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Worker(models.Model):
    """
    职工信息表
    """
    SEX = (
        ('male', '男'),
        ('female', '女')
    )
    WORK_STATUS = (
        (0, "未入职"),
        (1, "入职"),
        (2, "离职")
    )
    EDUCATION = (
        ('not', "无学历"),
        ('highschool', '高中'),
        ('university', '本科'),
        ('graduate', '研究生'),
        ('doctorate', '博士')
    )
    IS_CORE = (
        (0, '不是'),
        (1, '是')
    )
    IS_CHARGE = (
        (0, '不是'),
        (1, '是')
    )
    name = models.CharField(max_length=20, verbose_name="姓名")
    sex = models.CharField(max_length=6, choices=SEX,default="male", verbose_name="性别")
    birthday = models.DateField(verbose_name="出生日期")
    phone_number = models.CharField(max_length=11, verbose_name='手机号码')
    qq_number = models.CharField(max_length=11, verbose_name='QQ账号')
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    house_addr = models.CharField(max_length=100, verbose_name="户籍地址")
    card_number = models.CharField(max_length=20, verbose_name="身份证号码")
    education = models.CharField(max_length=15, default='not', verbose_name="学历")
    school = models.CharField(max_length=50,null=True, blank=True, verbose_name="毕业院校")
    work_status = models.IntegerField(choices=WORK_STATUS, default=0, verbose_name="在职状态")
    join_time = models.DateTimeField(verbose_name="入职时间")
    is_core = models.IntegerField(choices=IS_CORE, default=0, verbose_name="是否是核心成员")
    is_charge = models.IntegerField(choices=IS_CHARGE, default=0, verbose_name="是否主负责人")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name="职位")
    comment = models.ForeignKey(verbose_name="员工评价")
    department = models.ForeignKey(verbose_name="所属部门")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加记录时间")

    class Meta:
        verbose_name = "职工信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
