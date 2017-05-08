from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^request/', views.RequestView.as_view(), name='request'),
    url(r'^request-status$', views.UpdateRequest.as_view(), name='update_request')
]