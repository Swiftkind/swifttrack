from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^make-request$', views.RequestView.as_view(), name='request'),
    url(r'^request-status$', views.UpdateRequest.as_view(), name='update_request'),
    url(r'^dashboard/(?P<day>[0-9]+)/(?P<di>[\w-]+)/$', views.AdminView.as_view(), name='admin'),
    #url(r'^dashboard/(?P<day>)', views.AdminWorkDiariesView.as_view(), name='admin_work_diaries'),
    url(r'^confirm-account', views.ConfirmAccountView.as_view(), name='confirm_account'),
    url(r'^deactivate-account', views.DeactivateAccountView.as_view(), name='deactivate_account'),
    url(r'^employees/$', views.AllEmployeesView.as_view(), name='all_employees'),
    url(r'^employee/(?P<id>[0-9]+)', views.EmployeeProfileView.as_view(), name='employee_profile'),
    url(r'^view-requests$', views.ViewRequestsView.as_view(), name='view_all_requests'),
]