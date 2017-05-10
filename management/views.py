from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import RequestForm
from .models import Requests
from accounts.models import Account
from projects.models import WorkDiary
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

# Create your views here.

class RequestView(TemplateView):
	template_name = 'management/request.html'
	def get(self, request, *args, **kwargs):
		form = RequestForm(initial={'employee': request.user.id})
		requests_by_user = Requests.objects.filter(employee=request.user.id).order_by('-date_requested')
		requests = Requests.objects.all().order_by('-date_requested')
		return_data = {'form':form, 'requests':requests, 'requests_by_user': requests_by_user}
		return render(request, self.template_name, return_data)
	def post(self, request, *args, **kwargs):
		form = RequestForm(request.POST)
		if form.is_valid():
			form.save()
			form = RequestForm()
			requests_by_user = Requests.objects.filter(employee=request.user.id)
		return redirect('request')
		# 	return_data = {'form': form, 'success': 'Your request was successfully sent.', 'requests_by_user':requests_by_user}
		# 	return render(request, self.template_name, return_data)
		# return_data = {'form': form}
		# return render(request, self.template_name, return_data)

class UpdateRequest(TemplateView):
	def post(self, request, *args, **kwargs):
		id = request.POST['id']
		status = request.POST['status']
		confirmed = status or None
		Requests.objects.filter(id=id).update(confirmed=confirmed)
		# subject = 'Request for leave confirmation'
		# messages = 'Your request for leave with subject '+request.POST['subject']+' and content '+request.POST['content']+' was confirmed'
		# from_email = settings.EMAIL_HOST_USER
		return redirect('request')

class AdminView(TemplateView):
	template_name = 'management/admin.html'
	def get(self, request, *args, **kwargs):
		all_employees = Account.objects.filter(is_active=True)
		accounts_to_confirm = Account.objects.filter(is_active=False)
		return_data = {'all_employees': all_employees, 'accounts_to_confirm': accounts_to_confirm}
		return render(request, self.template_name, return_data)

class ConfirmAccountView(TemplateView):
	def post(self, request, *args, **kwargs):
		if request.POST.get('confirm') is not None:
			employee = request.POST['id']
			Account.objects.filter(id=employee).update(is_active=True)
			return redirect('admin')
		if request.POST.get('decline') is not None:
			employee = request.POST['id']
			account = Account.objects.get(id=employee)
			account.delete()
			return redirect('admin')

class DeactivateAccountView(TemplateView):
	def post(self, request, *args, **kwargs):
		employee = request.POST['id']
		Account.objects.filter(id=employee).update(is_active=False)
		return redirect('admin')

class EmployeeProfileView(TemplateView):
	template_name = 'management/employee-profile.html'
	def get(self, request, *args, **kwargs):
		employee_id = kwargs['id']
		employee = Account.objects.get(id=employee_id)
		return_data = {'employee': employee}
		return render(request, self.template_name, return_data)
