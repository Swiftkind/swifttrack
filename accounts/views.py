from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.views.generic import TemplateView
from .models import Account
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.
class RegistrationView(TemplateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            contact_number = form.cleaned_data['contact_number']
            
            form.save()
            return redirect('login')
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})

class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('https://github.com/regzimarx/', user=user)
            else:
                return_data = {'form': form, 'error': 'Can\'t login account. Invalid account credentials.'}
                return render(request, 'accounts/login.html', return_data)


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('/')