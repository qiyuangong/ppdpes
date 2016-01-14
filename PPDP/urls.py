from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^task/(?P<task_id>[0-9]+)$', views.task_detail, name='detail'),
    url(r'^anon(?P<anon_result_id>[0-9]+)$', views.anon_detail, name='anon_detail'),
    url(r'^eval(?P<eval_result_id>[0-9]+)$', views.eval_detail, name='eval_detail'),
    ]