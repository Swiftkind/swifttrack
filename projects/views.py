from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from . models import Project, ProjectAssignment, WorkDiary
from . forms import WorkDiaryForm


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/projects.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.filter(projectassignment=request.user.id)
        assignment = ProjectAssignment.objects.filter(employee_id=request.user.id)
        page = request.GET.get('page', 1)
        paginator = Paginator(assignment, 5)
        try:
            assignment = paginator.page(page)
        except PageNotAnInteger:
            assignment = paginator.page(1)
        except EmptyPage:
            assignment = paginator.page(paginator.num_pages)
        ctx_data = {
            'assignments': assignment,
            'projects': project,
        }
        return render(self.request, self.template_name, ctx_data)


class WorkDiaryView(TemplateView):
    template_name = 'projects/work_diary.html'

    def get(self, request, *args, **kwargs):
        form = WorkDiaryForm(initial={'project_assignment': kwargs['id']})
        project_assignment = ProjectAssignment.objects.get(id=kwargs['id'])
        works = WorkDiary.objects.filter(project_assignment=project_assignment).order_by('-date')
        query = request.GET.get('q')
        page = request.GET.get('page', 1)
        if query:
            works = works.filter(
                Q(finished_task__icontains=query)|
                Q(todo_task__icontains=query)|
                Q(issues__icontains=query)|
                Q(date__icontains=query)|
                Q(hours__icontains=query)
                ).distinct()
        paginator = Paginator(works, 5)
        try:
            works = paginator.page(page)
        except PageNotAnInteger:
            works = paginator.page(1)
        except EmptyPage:
            works = paginator.page(paginator.num_pages)
        ctx_data = {
            'form': form,
            'works': works,
            'project_assignment': project_assignment,
        }
        return render(self.request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        form = WorkDiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work-diary', id=kwargs['id'])
        ctx_data = {
            'form': form,
        }
        return render(self.request, self.template_name, ctx_data)