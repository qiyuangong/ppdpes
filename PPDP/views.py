from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Anon_Task, Anon_Result, Eval_Result

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def tasks(request):
    pass


def task_detail(request, task_id):
    try:
        task = Anon_Task.objects.get(pk=task_id)
    except Anon_Task.DoesNotExist:
        raise Http404("Task does not exist")
    # return render(request, )

def anon_detail(request, anon_result_id):
    try:
        anon_result = Anon_Result.objects.get(pk=anon_result_id)
    except Anon_Result.DoesNotExist:
        raise Http404("Anon_Result does not exist")
    # return render(request, )


def eval_detail(request, eval_result_id):
    try:
        eval_result = Eval_Result.objects.get(pk=eval_result_id)
    except Eval_Result.DoesNotExist:
        raise Http404("Eval_Result does not exist")
    # return render(request, )


