from datetime import datetime
from django import forms
from django.forms import extras
from django.forms import ModelForm, widgets

from .models import Requests, Misc
from projects.models import Project, ProjectAssignment


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
        fields = ['employee', 'project', 'weekly_hours']


class EditProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class EditProjectHoursForm(ModelForm):

    class Meta:
        model = ProjectAssignment
        fields = ['weekly_hours']

    def __init__(self, *args, **kargs):
        super(EditProjectHoursForm, self).__init__(*args, **kargs)
        self.fields['weekly_hours'].widget.attrs.update({'class' : 'form-control'})


class AddMiscForm(ModelForm):

    date_created = forms.DateField(
        widget=extras.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    class Meta:
        model = Misc
        fields = ['employees', 'name', 'types', 'total_amount', 'months', 'date_created']
