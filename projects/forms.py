from django import forms
from projects.models import Projects, WorkDiary


class WorkDiaryForm(forms.ModelForm):

    class Meta:
        model =  WorkDiary
        fields = [
<<<<<<< d0726ed2ff90c6479f493efe32061c8c2d7e36ec
            'user',
            'description',
            'hours',
            'project_id'
        ]
=======
            'description',
            'hours',
            'project_id',
        ]
>>>>>>> Added form on work diary feature
