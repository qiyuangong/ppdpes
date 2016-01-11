from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Anon_Task

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def tasks(request):
    pass


def task_detail(requst, task_id):
    try:
        task = Anon_Task.objects.get(pk=task_id)
    except Anon_Task.DoesNotExist:
        raise Http404("Task does not exist")
    # return render(requst, )

def anon_detail(requst, task_id):
    pass

def eval_detail(requst, task_id):
    pass

