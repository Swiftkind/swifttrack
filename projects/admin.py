from django.contrib import admin
from . models import Project, ProjectAssignment, WorkDiary, WorkDiaryLog


class ProjectsAdmin(admin.ModelAdmin):

    list_display = ['name', 'date_created', 'status']
    list_filter = ['date_created']


class ProjectAssignmentAdmin(admin.ModelAdmin):

    list_display = ['employee', 'project', 'weekly_hours', 'status']

class WorkDiaryAdmin(admin.ModelAdmin):

    list_display = ('finished_task', 'date', 'hours', )
    list_filter = ['date', 'hours']

class WorkDiaryLogAdmin(admin.ModelAdmin):

    list_display = ['work_diary', 'date_created']
    list_filter = ['date_created']

admin.site.register(Project, ProjectsAdmin)
admin.site.register(WorkDiary, WorkDiaryAdmin)
admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)
admin.site.register(WorkDiaryLog, WorkDiaryLogAdmin)
