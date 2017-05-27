from django import forms

from .models import Task, TaskLog


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = (
                  'memo',
                )