from django.shortcuts import render, get_object_or_404
# from fig_plot import cmp_multiple_result
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from models import Anon_Task, Anon_Result, Eval_Result, Data
from forms import add_task_form, add_data_form, UploadFileForm
from django.contrib.auth.decorators import login_required
import pdb


def task_update(request):
    task_id = request.GET['task_id']
    # end_time = request.GET['end_time']
    r_result = request.GET['result']
    anon_task = get_object_or_404(Anon_Task, pk=task_id)
    anon_task.end_time = timezone.now()
    if anon_task.task_type == 0:
        anon_id = anon_task.result_set
        anon_result = get_object_or_404(Anon_Result, pk=anon_id)
        anon_result.anon_result = r_result
        anon_result.end_time = anon_task.end_time
        anon_result.save()
    else:
        eval_id = anon_task.result_set
        eval_result = get_object_or_404(Eval_Result, pk=eval_id)
        eval_result.eval_result = r_result
        eval_result.end_time = anon_task.end_time
        eval_result.save()
    anon_task.save()
    response = {'status': 'success', 'retval': 'OK'}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def anon_index(request):
    anon_list = Anon_Result.objects.iterator()
    return render(request, 'PPDP/anon_index.html', {'anon_list': anon_list})


@login_required
def eval_index(request):
    eval_list = Eval_Result.objects.iterator()
    return render(request, 'PPDP/eval_index.html', {'eval_list': eval_list})


@login_required
def about(request):
    return render(request, 'PPDP/about.html')


@login_required
def add_task(request):
    if request.method == 'POST': # If the form has been submitted...
        form = add_task_form(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            # pdb.set_trace()
            return HttpResponseRedirect('/PPDP/') # Redirect after POST
    else:
        form = add_task_form()
    return render(request, 'PPDP/add_task.html', {'form': form})


@login_required
def add_data(request):
    if request.method == 'POST': # If the form has been submitted...
        form = add_data_form(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            # pdb.set_trace()
            return HttpResponseRedirect('/PPDP/') # Redirect after POST
    else:
        form = add_data_form()
    return render(request, 'PPDP/add_data.html', {'form': form})

@login_required
def index(request):
    task_list = Anon_Task.objects.iterator()
    return render(request, 'PPDP/index.html', {'task_list': task_list})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Anon_Task, pk=task_id)
    return render(request, 'PPDP/detail.html', {'task': task})


@login_required
def anon_detail(request, anon_result_id):
    anon_result = get_object_or_404(Anon_Result, pk=anon_result_id)
    parameters = json.loads(anon_result.anon_result)
    return render(request, 'PPDP/anon_detail.html',
                  {'anon_result': anon_result, 'parameters': parameters})


@login_required
def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            handle_uploaded_file(request.FILES['file_content'], title)

            data = Data.create(title, "tmp/" + str(title) + ".txt", request.POST['sa_index'],
                        request.POST['is_missing'], request.POST['is_high'], request.POST['is_rt'])
            data.save()
            return HttpResponseRedirect('/PPDP/')
    else:
        form = UploadFileForm()
    return render(request, 'PPDP/upload.html', {'form': form})



@login_required
def file_download(request, anon_result_id):
    anon_result = get_object_or_404(Anon_Result, pk=anon_result_id)
    temp = json.loads(anon_result.anon_result)
    file_url = temp['url']
    print anon_result.anon_result
    with open(file_url) as file:
        response = HttpResponse(file.read())
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_url.split('/')[-1])
        response['Content-Type'] = 'application/octet-stream'
        file.close()
        return response

@login_required
def eval_detail(request, eval_result_id):
    eval_re = get_object_or_404(Eval_Result, pk=eval_result_id)
    eval_result = json.loads(eval_re.eval_result)
    plot_result = dict()
    plot_result['ncp_k'] = cmp_multiple_result(eval_result[0], [eval_result[1]],
                               'K', 'NCP (%)', [str(eval_re.anon_algorithm.algorithm_text)], range(0, 65, 5))
    plot_result['time_k'] = cmp_multiple_result(eval_result[0], [eval_result[2]],
                                                'K', 'Time (s)', [str(eval_re.anon_algorithm.algorithm_text)])
    return render(request, 'PPDP/eval_detail.html', {'eval_result': eval_re, 'plot_result': plot_result})


# def ncp_k_plot(request, eval_result_id):
#     eval_re = get_object_or_404(Eval_Result, pk=eval_result_id)
#     eval_result = json.loads(eval_re.eval_result)
#     # print eval_result_id
#     return cmp_multiple_result(eval_result[0], [eval_result[1]],
#                                'K', 'NCP (%)', ['Mondrian'], range(0, 65, 5))
#
#     # return cmp_multiple_result([2, 5, 10, 25, 50, 100], [[7.51, 19.62, 28.52, 36.64, 45.2, 51.14],
#     #                                                      [3.18, 7.74, 12.86, 22.37, 31.4, 41.99]],
#     #                            'K', 'NCP (%)', ['Mondrian', 'Semi-Partition'], range(0, 65, 5))


def handle_uploaded_file(read_file, title='test'):
    with open("tmp/" + str(title) + ".txt", 'w') as destination:
        for chunk in read_file.chunks():
            destination.write(chunk)
    destination.close()


def cmp_multiple_result(xdata, ydatas, xname, yname, labels, yrange=range(0, 100, 10)):
    import matplotlib
    from django.http import HttpResponse
    matplotlib.use('Agg')
    import random
    from matplotlib import pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import base64
    from io import BytesIO
    font = {'family': 'monospace',
    'weight': 'bold',
    'size': 20}
    size = [8.33, 6.36]
    marksize = 15
    matplotlib.rc('font', **font)
    marker_style = ['s', '^', 'o', 'v', '*', '+', 'p']
    colors = ['b', 'r', 'c', 'g', 'm', 'y']
    line = ['-', '-', '-', '-']
    current_num = random.randint(1, 1000)
    fig = plt.figure(current_num, size)
    ls = len(labels)
    for i in range(ls):
        plt.plot(range(len(xdata)), ydatas[i], color=colors[i],
                linewidth=3.2, linestyle=line[i], marker=marker_style[i], ms=marksize, label=labels[i])
    plt.xticks(range(len(xdata)), xdata)
    plt.yticks(yrange)
    plt.ylabel(yname)
    plt.xlabel(xname)
    # axis([xdata[0], xdata[-1], 0, 40])
    plt.legend(loc='upper left', frameon=False, fontsize=20)
    # legend(loc='lower right')
    # legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    # ncol=2, mode="expand", borderaxespad=0.)
    plt.grid(True)
    # remove blank col caused by odd number
    plt.xlim(0, len(xdata) - 1)
    # fig.set_size_inches(size[0], size[1])
    # canvas = FigureCanvas(fig)
    # response=HttpResponse(content_type='image/png')
    # canvas.print_png(response)
    # fig.clf()
    # plt.close()
    # return response
    byte_io = BytesIO()
    plt.savefig(byte_io, format='png')
    byte_io.seek(0)  # rewind to beginning of file
    png_base64 = base64.b64encode(byte_io.getvalue())
    fig.clf()
    plt.close(current_num)
    return png_base64
