from .models import Worker, Comment, Salary

import xadmin
from xadmin import views

class WorkerAdmin(object):
    list_display = ['name', 'sex', 'birthday', 'phone_number', 'qq_number',
                    'email', 'house_addr', 'card_number', 'education', 'school',
                    'work_status', 'join_time', 'is_core', 'is_charge', 'job', 'department', 'add_time']
    search_fields  = ['name', 'sex', 'phone_number', 'qq_number',
                    'email', 'house_addr', 'card_number', 'education', 'school',
                    'work_status', 'is_core', 'is_charge', 'job', 'department',]
    list_filter = ['name', 'sex', 'birthday', 'phone_number', 'qq_number',
                    'email', 'house_addr', 'card_number', 'education', 'school',
                    'work_status', 'join_time', 'is_core', 'is_charge', 'job', 'department', 'add_time']
    list_editable = ['name', 'sex', 'birthday', 'phone_number', 'qq_number',
                    'email', 'house_addr', 'card_number', 'education', 'school',
                    'work_status', 'join_time', 'is_core', 'is_charge', 'job', 'department', 'add_time']
    model_icon = 'fa fa-address-card'


class CommentAdmin(object):
    list_display = ['worker', 'expect_requirements', 'is_meet', 'aspect', 'comment', 'comment_user',  'add_time']
    search_fields = ['expect_requirements', 'is_meet', 'aspect', 'comment', 'comment_user', 'worker']
    list_filter = ['expect_requirements', 'is_meet', 'aspect', 'comment', 'comment_user', 'worker', 'add_time']
    list_editable = ['expect_requirements', 'is_meet', 'aspect', 'comment', 'comment_user', 'worker', 'add_time']
    style_fields = {"expect_requirements": "ueditor", "comment": "ueditor"}
    model_icon = 'fa fa-comments'


class SalaryAdmin(object):
    list_display = ['worker', 'salary', 'achievements', 'has_pay', 'add_time']
    search_fields = ['worker', 'salary', 'achievements', 'has_pay']
    list_filter = ['worker', 'salary', 'achievements', 'has_pay', 'add_time']
    list_editable = ['worker', 'salary', 'achievements', 'has_pay', 'add_time']
    model_icon = 'fa fa-gratipay'


xadmin.site.register(Worker, WorkerAdmin)
xadmin.site.register(Salary, SalaryAdmin)
xadmin.site.register(Comment, CommentAdmin)