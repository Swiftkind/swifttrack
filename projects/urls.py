from django.conf.urls import url
from .views import ProjectView
from . import views

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    
]