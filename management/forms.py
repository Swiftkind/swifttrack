from django.forms import ModelForm, widgets
from .models import Requests
from projects.models import Project, ProjectAssignment
from datetime import datetime


class RequestForm(ModelForm):
    class Meta:
        model = Requests
        fields = ('employee', 'subject', 'date_of_leave', 'date_of_return', 'content')
        widgets = {
            'employee': widgets.TextInput(attrs={'type': 'hidden'}),
            'date_of_leave': widgets.DateTimeInput(attrs={'class':'form-control'}),
            'date_of_return': widgets.DateTimeInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kargs):
        super(RequestForm, self).__init__(*args, **kargs)
        self.fields['subject'].widget.attrs.update({'class' : 'form-control'})
        self.fields['content'].widget.attrs.update({'class' : 'form-control'})


class AddProjectForm(ModelForm):
 
    class Meta:
        model = Project
        fields = ['name',]


    def __init__(self, *args, **kargs):
        super(AddProjectForm, self).__init__(*args, **kargs)
        self.fields['name'].widget.attrs.update({'class' : 'form-control'})


class AssignEmployeeForm(ModelForm):
 
    class Meta:
        model = ProjectAssignment
        fields = ['employee', 'project', 'weekly_hours',]


    def __init__(self, *args, **kargs):
        super(AssignEmployeeForm, self).__init__(*args, **kargs)
        self.fields['employee'].widget.attrs.update({'class' : 'form-control'})
        self.fields['project'].widget.attrs.update({'class' : 'form-control'})
        self.fields['weekly_hours'].widget.attrs.update({'class' : 'form-control'})