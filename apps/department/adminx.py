from .models import Job, Department

import xadmin
from xadmin import views


class JobAdmin(object):
    list_display = ['name', 'description', 'expect_salary', 'is_core', 'worker_num', 'add_time']
    search_fields = ['name', 'description', 'expect_salary', 'is_core', 'worker_num']
    list_filter = ['name', 'description', 'expect_salary', 'is_core', 'add_time']
    list_editable = ['name', 'description', 'expect_salary', 'is_core', 'add_time']
    style_fields = {"description": "ueditor"}
    model_icon = 'fa fa-tags'


class DepartmentAdmin(object):
    list_display = ['name', 'duty', 'description', 'create_time', 'vision','worker_num', 'add_time',]
    search_fields = ['name', 'duty', 'description', 'create_time', 'vision', 'worker_num']
    list_filter = ['name', 'duty', 'description', 'create_time', 'vision', 'add_time']
    list_editable = ['name', 'duty', 'description', 'create_time', 'vision', 'add_time']
    # readonly_fields = ['get_worker_num']
    style_fields = {"description": "ueditor", "vision": "ueditor"}
    model_icon = 'fa fa-building'


xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(Job, JobAdmin)