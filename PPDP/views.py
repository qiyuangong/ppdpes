from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from fig_plot import cmp_multiple_result

from .models import Anon_Task, Anon_Result, Eval_Result

def index(request):
    task_list = Anon_Task.objects.iterator()
    context = {'task_list': task_list}
    return render(request, 'PPDP/index.html', context)


def task_detail(request, task_id):
    task = get_object_or_404(Anon_Task, pk=task_id)
    return render(request, 'PPDP/detail.html', {'task': task})


def anon_detail(request, anon_result_id):
    anon_result = get_object_or_404(Anon_Result, pk=anon_result_id)
    return render(request, 'PPDP/anon_detail.html', {'anon_result': anon_result})


def eval_detail(request, eval_result_id):
    eval_result = get_object_or_404(Eval_Result, pk=eval_result_id)
    return render(request, 'PPDP/eval_detail.html', {'eval_result': eval_result})


def ncp_k_plot(request):
    return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
                                                         [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
                               'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], range(0, 65, 5))

def ncp_qi_plot(request):
    return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
                                                         [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
                               'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], 'semi_ncp_k', range(0, 65, 5))

def ncp_size_plot(request):
    return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
                                                         [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
                               'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], 'semi_ncp_k', range(0, 65, 5))

def time_k_plot(request):
    return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
                                                         [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
                               'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], range(0, 65, 5))

def time_qi_plot(request):
    return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
                                                         [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
                               'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], 'semi_ncp_k', range(0, 65, 5))

def time_size_plot(request):
    return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
                                                         [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
                               'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], 'semi_ncp_k', range(0, 65, 5))
