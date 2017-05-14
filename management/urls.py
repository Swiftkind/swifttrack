from django.conf.urls import url, include
from . import views
from .views import ProjectManageView, AddProjectView, AssignEmployeeView

urlpatterns = [
    url(r'^request/create$', views.RequestView.as_view(), name='request'),
    url(r'^request/confirm$', views.UpdateRequest.as_view(), name='update_request'),
    url(r'^dashboard/(?P<day>[0-9]+)/$', views.AdminView.as_view(), name='admin'),
    #url(r'^dashboard/(?P<day>)', views.AdminWorkDiariesView.as_view(), name='admin_work_diaries'),
    url(r'^account/confirm', views.ConfirmAccountView.as_view(), name='confirm_account'),
    url(r'^account/deactivate', views.DeactivateAccountView.as_view(), name='deactivate_account'),
    url(r'^employees/$', views.AllEmployeesView.as_view(), name='all_employees'),
    url(r'^employee/(?P<id>[0-9]+)', views.EmployeeProfileView.as_view(), name='employee_profile'),
    url(r'^requests/view$', views.ViewRequestsView.as_view(), name='view_all_requests'),
    url(r'^projects/(?P<id>[0-9]+)/$', views.ProjectManageView.as_view(), name='view_projects'),
    url(r'^payroll/$', views.ManagementPayrollView.as_view(), name='management_payroll'),
    url(r'^payroll/update$', views.ManagementPayrollView.as_view(), name='update_payroll'),
    url(r'^payroll/report/(?P<id>[0-9]+)/$', views.PayrollReportView.as_view(), name='payroll_report'),
    url(r'^add/project/$', AddProjectView.as_view(), name='add_project'),
    url(r'^projects/(?P<id>[0-9]+)/assign/employee/$', AssignEmployeeView.as_view(), name='assign_employee'),

]