from django import forms
from projects.models import Projects, WorkDiary
from django.forms import widgets, ModelForm

class WorkDiaryForm(ModelForm):

    class Meta:
        model =  WorkDiary
        fields = [
            'user',
            'description',
            'hours',
            # 'project',
        ]
        widgets = {
            'user': widgets.TextInput(attrs={'type': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super(WorkDiaryForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

class AddProjectForm(ModelForm):

    class Meta:
        model = Projects
        fields = ['user', 'name', 'hours', 'hours_spent']
        widgets = {
            'user': widgets.TextInput(attrs={'type': 'hidden'}),
        }

    def __init__(self, *args, **kargs):
        super(AddProjectForm, self).__init__(*args, **kargs)
        self.fields['name'].widget.attrs.update({'class' : 'form-control'})