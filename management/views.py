from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import RequestForm
from .models import Requests

# Create your views here.

class RequestView(TemplateView):
	template_name = 'management/request.html'
	def get(self, request, *args, **kwargs):
		form = RequestForm(initial={'employee': request.user})
		requests = Requests.objects.all()
		return_data = {'form':form, 'requests':requests}
		return render(request, self.template_name, return_data)
	def post(self, request, *args, **kwargs):
		form = RequestForm(request.POST)
		if form.is_valid():
			form.save()
			form = RequestForm()
			return_data = {'form': form, 'success': 'Your request was successfully sent.'}
			return render(request, self.template_name, return_data)
		return_data = {'form': form}
		return render(request, self.template_name, return_data)