from django.conf.urls import url
from .views import ProjectView, WorkDiaryView, WorkDiaryEditView, EmployeesMiscView, WorkDiaryLogView

from . import views

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    url(r'^work_diary/(?P<id>[0-9]+)/$', WorkDiaryView.as_view(), name='work-diary'),
    url(r'^work_diary/(?P<id>[0-9]+)/edit/(?P<work_diary_id>[0-9]+)/$', WorkDiaryEditView.as_view(), name='edit-work-diary'),
    url(r'^misc/$', EmployeesMiscView.as_view(), name='employees_misc'),
    url(r'^work_diary/(?P<work_diary_id>[0-9]+)/log/$', WorkDiaryLogView.as_view(), name='work_diary_log'),
]
