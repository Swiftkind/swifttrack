from django.forms import ModelForm
from .models import Requests
from django.forms import widgets

class RequestForm(ModelForm):
	class Meta:
		model = Requests
		fields = ('employee', 'subject', 'date_of_leave', 'content')
		widgets = {
            'date_of_leave': widgets.DateTimeInput(attrs={'type': 'date', 'class':'form-control'}),
            'employee': widgets.TextInput(attrs={'type': 'hidden'}),
        }

	def __init__(self, *args, **kargs):
	    super(RequestForm, self).__init__(*args, **kargs)
	    self.fields['employee'].widget.attrs.update({'class' : 'form-control'})
	    self.fields['subject'].widget.attrs.update({'class' : 'form-control'})
	    self.fields['content'].widget.attrs.update({'class' : 'form-control'})
