import xadmin
from xadmin import views

class Admin(object):
    list_display = []
    search_fields = []
    list_filter = []
    list_editable = []
    model_icon = ''

class Admin(object):
    list_display = []
    search_fields = []
    list_filter = []
    list_editable = []
    model_icon = ''

xadmin.site.register(, Admin)