from django import forms
from projects.models import Project, WorkDiary, ProjectAssignment
from django.forms import widgets, ModelForm

class WorkDiaryForm(forms.ModelForm):

    project_assignment = forms.ModelChoiceField(
        queryset=ProjectAssignment.objects.all(),
        widget=forms.TextInput(attrs={'type':'hidden'})
    )

    class Meta:
        model =  WorkDiary
        fields = [
            'project_assignment',
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
        self.fields['hours'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
        self.fields['project_assignment'].label = ''

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})