from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^project/(?P<project_id>[0-9]+)/tasks/', views.TaskListView.as_view(), name='project_task_list'),
    url(r'^project/(?P<project_id>[0-9]+)/task-create/', views.TaskCreateFormView.as_view(), name='project_task_create'),
    url(r'^project/(?P<project_id>[0-9]+)/task/(?P<task_id>[0-9]+)/update/', views.TaskUpdateFormView.as_view(), name='project_task_update'),

    url(r'^project/(?P<project_id>[0-9]+)/task/(?P<task_id>[0-9]+)/delete/', views.TaskDeleteView.as_view(), name='project_task_delete'),
    url(r'^project/(?P<project_id>[0-9]+)/task/(?P<task_id>[0-9]+)/timein/', views.TaskTimeInView.as_view(), name='project_task_timein'),
    url(r'^project/(?P<project_id>[0-9]+)/task/(?P<task_id>[0-9]+)/timeout/', views.TaskTimeInView.as_view(), name='project_task_timeout'),
    url(r'^project/(?P<project_id>[0-9]+)/task/(?P<task_id>[0-9]+)/mark-as-done/', views.TaskMarkAsDoneView.as_view(), name='project_task_mark_as_done'),

    url(r'^tasks/(?P<task_id>[0-9]+)/logs/', views.TaskLogListView.as_view(), name='task_logs_list'),
]