from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^profile/$', views.AccountView.as_view(), name='profile'),
    url(r'^profile/update-account/$', views.UpdateAccountView.as_view(), name='update_account'),
    url(r'^profile/update-password/$', views.UpdatePasswordView.as_view(), name='update_password'),
    url(r'^account/payroll/$', views.PayrollView.as_view(), name='payroll'),
    url(r'^account/payroll/add/$', views.AddPayrollView.as_view(), name='add-payroll')
]