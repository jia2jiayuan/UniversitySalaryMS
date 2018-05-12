from django.contrib.auth.hashers import make_password
from .models import Manager

from .models import Manager, Worklog

import xadmin
from xadmin import views


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
    list_display = ['username', 'name', 'image', 'sex', 'birthday', 'phone_number', 'qq_number',
                    'work_description', 'join_time', 'worklog_num','add_time']
    # 可搜索字段
    search_fields = ['username', 'name', 'image', 'sex', 'birthday',
                     'phone_number', 'qq_number', 'work_description']
    # 可过滤字段
    list_filter = ['username', 'name', 'image', 'sex', 'birthday',
                   'phone_number', 'qq_number', 'work_description', 'join_time', 'add_time']
    # 可编辑字段
    list_editable = ['name', 'sex', 'birthday', 'phone_number',
                     'qq_number', 'work_description', 'join_time',]
    style_fields = {"work_description": "ueditor"}
    # ordering = ['-fav_num']
    # 表上小小图标
    model_icon = 'fa fa-adn'

    def save_models(self):
        # 可以在保存课程实例的时候，做些任务，像触发器.新增和修改都会走这个流程
        # 如以下保存机构中course_num课程数量统计
        obj = self.new_obj
        print(obj.password)
        # 获取初始密码
        if Manager.objects.filter(id=obj.id):
            raw_password = Manager.objects.get(id=obj.id).password

        # 获取保存时候密码
        new_password = obj.password
        print("new_password:", new_password)
        # 如果两者不相同，则认为修改了密码，重新进行sha1加密
        if raw_password != new_password:
            obj.password = make_password(obj.password)
        # print(obj.password)
        obj.save()
        # odj.save()
        # if obj:
        #   course_org = obj.course_org
        #   course_org.course_num = Course.objects.filter(course_org=course_org).count()
        #   course_org.save()
        pass


class WorklogAdmin(object):
    list_display = ['name', 'content', 'start_time', 'end_time', 'has_finished', 'manager', 'add_time']
    search_fields = ['name', 'content', 'has_finished',]
    list_filter = ['name', 'content', 'start_time', 'end_time', 'has_finished', 'manager', 'add_time']
    list_editable = ['name', 'content', 'start_time', 'end_time', 'has_finished', 'manager', 'add_time']
    style_fields = {"content": "ueditor"}
    model_icon = 'fa fa-pied-piper-alt'


# 全局注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, CommonSetting)

# Manger注册
xadmin.site.unregister(Manager)
xadmin.site.register(Manager, ManagerAdmin)
xadmin.site.register(Worklog, WorklogAdmin)