from django.conf.urls import url
from .views import ProjectView, WorkDiaryView, WorkDiaryEditView
from . import views

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    url(r'^work_diary/(?P<id>[0-9]+)/$', WorkDiaryView.as_view(), name='work-diary'),
    url(r'^work_diary/(?P<id>[0-9]+)/edit/(?P<work_diary_id>[0-9]+)/$', WorkDiaryEditView.as_view(), name='edit-work-diary'),
]