from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ProjectView.as_view(), name='project'),
    url(r'^work_diary/(?P<id>[0-9]+)/$', views.WorkDiaryView.as_view(), name='work-diary'),
    url(r'^work_diary/(?P<id>[0-9]+)/edit/(?P<work_diary_id>[0-9]+)/$', views.WorkDiaryEditView.as_view(), name='edit-work-diary'),
    url(r'^work_diary/(?P<work_diary_id>[0-9]+)/log/$', views.WorkDiaryLogView.as_view(), name='work_diary_log'),
    url(r'^misc/$', views.EmployeesMiscView.as_view(), name='employees_misc'),
]
