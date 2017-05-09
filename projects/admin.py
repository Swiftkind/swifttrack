from django.contrib import admin
from . models import Projects, WorkDiary


class ProjectsAdmin(admin.ModelAdmin):

    list_display = ('name', 'date', 'hours',)
    list_filter = ['date', 'hours']


class WorkDiaryAdmin(admin.ModelAdmin):

    list_display = ('description', 'date', 'hours', )
    list_filter = ['date', 'hours']

admin.site.register(Projects, ProjectsAdmin)
admin.site.register(WorkDiary, WorkDiaryAdmin)