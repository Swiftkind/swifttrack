from django.forms import ModelForm, widgets
from .models import Requests
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