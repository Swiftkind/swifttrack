from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register$', views.RegistrationView.as_view(), name='registration'),
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout', views.LogoutView.as_view(), name="logout")
]