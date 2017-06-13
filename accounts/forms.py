from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ( UserCreationForm,
                                        UserChangeForm,
                                        PasswordChangeForm,
                                        )

from .models import Account, Payroll

class UserProfileForm(ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'address', 'contact_number', 'profile_pic', 'about_me')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control', 'pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control', 'pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '})
        self.fields['address'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact_number'].widget.attrs.update({'class' : 'form-control', 'pattern':'[0-9 ]+', 'title':'Enter Number Only '})
        self.fields['profile_pic'].widget.attrs.update({'class' : 'form-control'})
        self.fields['about_me'].widget.attrs.update({'class' : 'form-control'})

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'address', 'contact_number', 'profile_pic', 'about_me')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['address'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact_number'].widget.attrs.update({'class' : 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class' : 'form-control'})
        self.fields['about_me'].widget.attrs.update({'class' : 'form-control'})


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['address'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contact_number'].widget.attrs.update({'class' : 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class' : 'form-control'})
        self.fields['about_me'].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'address', 'contact_number', 'profile_pic', 'about_me', 'password')

class LoginForm(forms.Form):
    user_cache = None
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Invalid Email or Password")
        else:
            self.user_cache = user
        return self.cleaned_data

class AddPayrollForm(ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'date', 'description']
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'date', 'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddPayrollForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class' : 'form-control'})
        self.fields['employee'].widget.attrs.update({'class' : 'form-control'})
