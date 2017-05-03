from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from . models import Projects


class ProjectView(LoginRequiredMixin, TemplateView):

    model = Projects
    template_name = 'project/projects.html'

    def get(self, request, *args, **kwargs):
        project = Projects.objects.filter(user=self.request.user).order_by('-date')
        context = {
            'projects': project,
        }
        return render(self.request, self.template_name, context)