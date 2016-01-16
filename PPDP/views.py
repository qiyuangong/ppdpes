from django.shortcuts import render, get_object_or_404
# from fig_plot import cmp_multiple_result
import json
from django.http import HttpResponse, HttpResponseRedirect

from models import Anon_Task, Anon_Result, Eval_Result
from forms import add_task_form
import pdb


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


def index(request):
    task_list = Anon_Task.objects.iterator()
    context = {'task_list': task_list}
    return render(request, 'PPDP/index.html', context)


def task_detail(request, task_id):
    task = get_object_or_404(Anon_Task, pk=task_id)
    return render(request, 'PPDP/detail.html', {'task': task})


def anon_detail(request, anon_result_id):
    anon_result = get_object_or_404(Anon_Result, pk=anon_result_id)
    parameters = json.loads(anon_result.anon_result)
    return render(request, 'PPDP/anon_detail.html',
                  {'anon_result': anon_result, 'parameters': parameters})


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


def eval_detail(request, eval_result_id):
    eval_re = get_object_or_404(Eval_Result, pk=eval_result_id)
    eval_result = json.loads(eval_re.eval_result)
    plot_result = dict()
    plot_result['ncp_k'] = cmp_multiple_result(eval_result[0], [eval_result[1]],
                               'K', 'NCP (%)', ['Mondrian'], range(0, 65, 5))
    plot_result['time_k'] = cmp_multiple_result(eval_result[0], [eval_result[2]],
                                                'K', 'Time (s)', ['Mondrian'])
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
