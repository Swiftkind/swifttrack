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
            'project',
        ]
        widgets = {
            'user': widgets.TextInput(attrs={'type': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super(WorkDiaryForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})