from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^request/', views.RequestView.as_view(), name='request'),
    url(r'^request-status$', views.UpdateRequest.as_view(), name='update_request'),
    url(r'^dashboard', views.AdminView.as_view(), name='admin'),
    url(r'^confirm-account', views.ConfirmAccountView.as_view(), name='confirm_account'),
    url(r'^deactivate-account', views.DeactivateAccountView.as_view(), name='deactivate_account'),
    url(r'^employee/(?P<id>[0-9]+)', views.EmployeeProfileView.as_view(), name='employee_profile'),
]