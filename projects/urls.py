from django.conf.urls import url
from .views import ProjectView, WorkDiaryView, WorkReportView
from . import views

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    url(r'^work-diary/$', WorkDiaryView.as_view(), name='work-diary'),
    url(r'^reports/$', WorkReportView.as_view(), name='reports'),
]