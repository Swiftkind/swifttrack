from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import LoginForm, AddPayrollForm
from .models import Account, Payroll
from .mixins import AccountTimestamp


class RegistrationView(TemplateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})

class LoginView(AccountTimestamp, TemplateView):
    template_name = 'accounts/login.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return render(self.request, self.template_name, {
                'form': LoginForm(),
            })
        return redirect('profile')

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            login(self.request, form.user_cache)
            if form.user_cache.is_staff:
                return redirect('admin', day=0)
            self.record(self.request)
            return redirect('project')
        return render(self.request, self.template_name, {'form': form})

class LogoutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('/project/accounts/')

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

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
        return redirect('project')

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

class PayrollView(TemplateView):
    template_name = 'accounts/payroll.html'

    def get(self, request, *args, **kwargs):
        payroll = Payroll.objects.filter(employee_id=request.user.id).order_by('-date')
        return_data = {'payroll': payroll}
        return render(request, self.template_name, return_data)

class AddPayrollView(TemplateView):
    template_name = 'accounts/add-payroll.html'

    def get(self, request, *args, **kwargs):
        form = AddPayrollForm()
        return_data = {'form': form}
        return render(request, self.template_name, return_data)

    def post(self, request, *args, **kwargs):
        form = AddPayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll')
        return_data = {'form': form, 'error': 'Can\'t add payroll'}
        return render(request, self.template_name, return_data)