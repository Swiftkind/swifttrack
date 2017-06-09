from django.contrib import admin

from . import models


class TaskLogInline(admin.TabularInline):
    model = models.TaskLog


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'memo', 'mark_as_done', 'log')
    inlines = [TaskLogInline,]


admin.site.register(models.Task, TaskAdmin)