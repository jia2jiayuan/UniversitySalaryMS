from django.db import models
from datetime import datetime



class Job(models.Model):
    """
    职位信息表
    """
    IS_CORE = (
        (0, '不是'),
        (1, '是')
    )
    name = models.CharField(max_length=20, verbose_name="职位名")
    description = models.TextField(null=True, blank=True,verbose_name="部门描叙")
    # description = UEditorField(verbose_name="工作描叙", imagePath='job/images/%Y/%m', width=1000,
    #                          height=300, filePath='job/files/%Y/%m')
    expect_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="预估工资")
    is_core = models.IntegerField(choices=IS_CORE, default=0, verbose_name="是否是核心职位")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加记录时间")

    class Meta:
        verbose_name = "职位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取职位相关的员工数量
    def worker_num(self):
        return self.worker_set.all().count()
    worker_num.short_description = "职位员工数"


class Department(models.Model):
    """
    部门信息表
    """
    name = models.CharField(max_length=20, verbose_name="部门名")
    duty = models.CharField(max_length=200, verbose_name="部门职责")
    description = models.TextField(null=True, blank=True, verbose_name="部门描叙")
    # description = UEditorField(verbose_name="部门描叙", imagePath='department/images/%Y/%m', width=1000,
    #                          height=300, filePath='department/files/%Y/%m', null=True, blank=True)
    create_time = models.DateField(verbose_name="创建时间")
    vision = models.TextField(null=True, blank=True, verbose_name="部门愿景")
    # vision = UEditorField(verbose_name="部门愿景", imagePath='department/images/%Y/%m', width=1000,
    #                          height=300, filePath='department/files/%Y/%m', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加记录时间")

    class Meta:
        verbose_name = "部门信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取部门员工数
    def worker_num(self):
        return self.worker_set.all().count()
    worker_num.short_description = "部门员工数"