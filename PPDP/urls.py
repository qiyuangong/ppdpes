from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='ppdp_index'),
    url(r'^anon_index$', views.anon_index, name='anon_index'),
    url(r'^eval_index$', views.eval_index, name='eval_index'),
    url(r'^add_task$', views.add_task, name='add_task'),
    url(r'^add_data$', views.add_data, name='add_data'),
    url(r'^task_update', views.task_update, name='task_update'),
    url(r'^task/(?P<task_id>[0-9]+)$', views.task_detail, name='detail'),
    url(r'^anon(?P<anon_result_id>[0-9]+)$', views.anon_detail, name='anon_detail'),
    url(r'^eval(?P<eval_result_id>[0-9]+)$', views.eval_detail, name='eval_detail'),
    url(r'^upload$', views.file_upload, name='file_upload'),
    url(r'^upload_gh/(?P<data_id>[0-9]+)$', views.gh_upload, name='gh_upload'),
    url(r'^about', views.about, name='about'),
    ]

# url(r'^anon(?P<anon_result_id>[0-9]+)/anon_data.txt$', views.file_download, name='file_download'),
