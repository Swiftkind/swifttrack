from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import Projects, WorkDiary


class ProjectView(LoginRequiredMixin, TemplateView):

    model = Projects
    template_name = 'project/projects.html'

    def get(self, request, *args, **kwargs):
        project = Projects.objects.all().order_by('-date')
        ctx_data = {
            'projects': project,
        }
        return render(self.request, self.template_name, ctx_data)


class WorkDiaryView(TemplateView):

    model = WorkDiary
    template_name = 'project/work_diary.html'

    def get(self, request, *args, **kwargs):
        work = WorkDiary.objects.all()
        ctx_data = {
            'works': work,
        }
        return render(self.request, self.template_name, ctx_data)