from django.contrib import admin
from .models import *


class UsersAdmin(admin.ModelAdmin):
    fields = ('uphone', 'uemail', 'uname', 'isActive')
    search_fields = ('uname',)

# Register your models here.
admin.site.register(Users, UsersAdmin)
