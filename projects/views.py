from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import Projects, WorkDiary
from . forms import WorkDiaryForm


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
        form = WorkDiaryForm()
        work = WorkDiary.objects.all()
        ctx_data = {
            'works': work,
            'form': form,
        }
        return render(self.request, self.template_name, ctx_data)
<<<<<<< d0726ed2ff90c6479f493efe32061c8c2d7e36ec
=======

    def post(self, request, *args, **kwargs):
        form = WorkDiaryForm()
        if form.is_valid():
            form.save()
            return redirect('/project/')
        return HttpResponse('Error!')
>>>>>>> Added form on work diary feature
