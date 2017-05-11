from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from . models import Project, ProjectAssignment, WorkDiary
from . forms import WorkDiaryForm


class ProjectView(LoginRequiredMixin, TemplateView):

    model = Project, ProjectAssignment
    template_name = 'projects/projects.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.filter(user=request.user.id)
        assignment = ProjectAssignment.objects.filter(employee=request.user.id)
        ctx_data = {
            'assignments': assignment,
            'project': project,
        }
        return render(self.request, self.template_name, ctx_data)


class WorkDiaryView(TemplateView):

    form_class = WorkDiaryForm
    model = WorkDiary, Project
    template_name = 'projects/work_diary.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'user': request.user.id})
        assignment = ProjectAssignment.objects.filter(id=request.user.id)
        work = WorkDiary.objects.all()
        query = self.request.GET.get('q')
        if query:
            work = work.filter(
                Q(finished_task__icontains=query)|
                Q(todo_task__icontains=query)|
                Q(issues__icontains=query)|
                Q(date__icontains=query)|
                Q(hours__icontains=query)
                ).distinct()
        ctx_data = {
            'form': form,
            'work': work,
            'id': kwargs['id'],
            'assignments': assignment,
        }
        return render(self.request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/project/')
        ctx_data = {
            'form': form,
        }
        return render(self.request, self.template_name, ctx_data)