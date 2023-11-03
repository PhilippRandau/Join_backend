from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Join.models import Task,Category


admin.site.register(Task)
admin.site.register(Category)

