
from .models import Manager, Worklog

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin


class BaseSetting(object):
    """
    是否使用主题
    """
    enable_themes = True
    use_bootswatch = True


class CommonSetting(object):
    """
    更改后台的标题和落脚，并且让菜单可以收起来
    """
    # 后台标题
    site_title = '大学工资管理系统'
    # 后台落脚
    site_footer = 'UniversitySalaryMS'
    # 收缩菜单
    menu_style = 'accordion'


class ManagerAdmin(object):
    """管理员表后台注册"""
    # 显示字段
    list_display = ['username', 'name', 'image', 'sex', 'birthday', 'phone_number', 'qq_number', 'work_description', 'join_time', 'add_time']
    # 可搜索字段
    search_fields = ['username', 'name', 'image', 'sex', 'birthday', 'phone_number', 'qq_number', 'work_description']
    # 可过滤字段
    list_filter = ['username', 'name', 'image', 'sex', 'birthday', 'phone_number', 'qq_number', 'work_description', 'join_time', 'add_time']
    # 可编辑字段
    list_editable = ['name', 'sex', 'birthday', 'phone_number', 'qq_number', 'work_description', 'join_time',]
    # 表上小小图标
    model_icon = 'fa fa-picture-o'


class WorklogAdmin(object):
    list_display = ['name', 'content', 'start_time', 'end_time', 'has_finished', 'manager', 'add_time']
    search_fields = ['name', 'content', 'has_finished',]
    list_filter = ['name', 'content', 'start_time', 'end_time', 'has_finished', 'manager', 'add_time']
    list_editable = ['name', 'content', 'start_time', 'end_time', 'has_finished', 'manager', 'add_time']
    model_icon = 'fa fa-picture-o'

# 全局注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, CommonSetting)

# Manger注册
xadmin.site.unregister(Manager)
xadmin.site.register(Manager, ManagerAdmin)
xadmin.site.register(Worklog, WorklogAdmin)