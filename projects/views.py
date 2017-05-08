from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import Projects, WorkDiary
from . forms import WorkDiaryForm
from django.db.models import F


class ProjectView(LoginRequiredMixin, TemplateView):

    model = Projects
    template_name = 'project/projects.html'

    def get(self, request, *args, **kwargs):
        project = Projects.objects.filter(user=request.user)
        ctx_data = {
            'projects': project,
        }
        return render(self.request, self.template_name, ctx_data)


class WorkDiaryView(TemplateView):

    form_class = WorkDiaryForm
    model = WorkDiary, Projects
    template_name = 'project/work_diary.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'user': request.user.id})
        work = WorkDiary.objects.filter(user=request.user.id)
        ctx_data = {
            'form': form,
            'work': work,
        }
        return render(self.request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            hs = request.POST['hours']
            p = request.POST['project']
            Projects.objects.filter(id=p).update(hours_spent=F('hours_spent')+hs)
            return redirect('/project/')
        form = self.form_class()
        return render(self.request, self.template_name, {'form': form})


class WorkReportView(TemplateView):

    template_name = 'project/work_detail.html'

    def get(self, request, *args, **kwargs):
        work = WorkDiary.objects.filter(user=request.user).order_by('-date')
        return render(request, self.template_name, {'work': work})
