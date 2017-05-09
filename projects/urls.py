from django.conf.urls import url
from .views import ProjectView, AddProjectView, WorkDiaryView, ReportsYearArchiveView, ReportsWeekArchiveView
from django.views.generic.dates import ArchiveIndexView
from .models import WorkDiary
from . import views

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name='project'),
    url(r'^add-project$', AddProjectView.as_view(), name='add-project'),
    url(r'^work_diary/(?P<id>[0-9]+)/$', WorkDiaryView.as_view(), name='work-diary'),
    url(r'^reports/$',
        ArchiveIndexView.as_view(model=WorkDiary, date_field="date"),
        name="reports_archive"),
    url(r'^reports/(?P<year>[0-9]{4})/$', ReportsYearArchiveView.as_view(), name='reports_year_archive'),
    url(r'^reports/(?P<year>[0-9]{4})/(?P<week>[0-9]+)/$', ReportsWeekArchiveView.as_view(), name="archive_week"),
]