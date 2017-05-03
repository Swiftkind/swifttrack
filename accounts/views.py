from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import TemplateView
from .models import Account, Payroll
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#Registration view
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
#Login view
class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('account')
        else:
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
                return redirect('account')
            else:
                return_data = {'form': form, 'error': 'Can\'t login account. Invalid account credentials.'}
                return render(request, self.template_name, return_data)

#Logout view
class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('/')

#Account view
class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

#Update account view
class UpdateAccountView(TemplateView):
    template_name = 'accounts/update_account.html'
    def get(self, request, *args, **kwargs):
        form = CustomUserChangeForm(instance=request.user)
        change_pass_form = PasswordChangeForm(user=request.user)
        return_data = {'form': form, 'change_pass_form': change_pass_form}
        return render(request, self.template_name, return_data)
    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('account')

#Update password view
class UpdatePasswordView(TemplateView):
    template_name = 'accounts/update_password.html'
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        return_data = {'form': form}
        return render(request, self.template_name, return_data)
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('account')
        return_data = {'form': form}
        return render(request, self.template_name, return_data)

#Payroll view
class PayrollView(TemplateView):
    template_name = 'accounts/payroll.html'
    def get(self, request, *args, **kwargs):
        payroll = Payroll.objects.filter(employee_id=request.user)
        return_data = {'payroll':payroll}
        return render(request, self.template_name, return_data)