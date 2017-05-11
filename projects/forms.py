from django import forms
from projects.models import Project, WorkDiary
from django.forms import widgets, ModelForm

class WorkDiaryForm(forms.ModelForm):

    class Meta:
        model =  WorkDiary
        fields = [
            # 'project_assignment',
            'finished_task',
            'todo_task',
            'issues',
            'hours',
        ]

    def __init__(self, *args, **kwargs):
        super(WorkDiaryForm, self).__init__(*args, **kwargs)
        self.fields['finished_task'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
        self.fields['todo_task'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
        self.fields['issues'].widget.attrs.update({'class': 'form-control', 'rows': '3'})