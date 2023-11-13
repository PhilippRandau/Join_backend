from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Join.models import Task, Category, Subtask


class AssignedTo(admin.ModelAdmin):
    filter_horizontal = ('assigned_to', 'subtask')


admin.site.register(Task, AssignedTo)
admin.site.register(Category)
admin.site.register(Subtask)
