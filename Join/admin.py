from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Join.models import Task,Category
class AssignedTo(admin.ModelAdmin):
    filter_horizontal = ('assigned_to',)

admin.site.register(Task, AssignedTo)
admin.site.register(Category)


