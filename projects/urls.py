from django.conf.urls import url
from .views import ProjectView, WorkDiaryView, Reports
from . import views

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    url(r'^work_diary/$', WorkDiaryView.as_view(), name='work_diary'),
    url(r'^reports/$', Reports.as_view(), name='reports'),
]