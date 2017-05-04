from django import forms
from projects.models import Projects, WorkDiary


class WorkDiaryForm(forms.ModelForm):

    class Meta:
        model =  WorkDiary
        fields = [
            'user',
            'description',
            'hours',
            'project',
        ]
