from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^task/(?P<task_id>[0-9]+)$', views.task_detail, name='detail'),
    url(r'^anon(?P<anon_result_id>[0-9]+)$', views.anon_detail, name='anon_detail'),
    url(r'^eval(?P<eval_result_id>[0-9]+)$', views.eval_detail, name='eval_detail'),
    url(r'^ncp_k.png$', views.ncp_k_plot),
    url(r'^ncp_qi.png$', views.ncp_qi_plot),
    url(r'^ncp_size.png$', views.ncp_size_plot),
    url(r'^time_k.png$', views.time_k_plot),
    url(r'^time_qi.png$', views.time_qi_plot),
    url(r'^time_size.png$', views.time_size_plot),
    ]