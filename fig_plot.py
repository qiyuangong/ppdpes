import matplotlib
import django
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

font = {'family': 'monospace',
        'weight': 'bold',
        'size': 20}
size = [8.33, 6.36]
marksize = 15
matplotlib.rc('font', **font)
marker_style = ['s', '^', 'o', 'v', '*', '+', 'p']
colors = ['b', 'r', 'c', 'g', 'm', 'y']
line = ['-', '-', '-', '-']


def cmp_multiple_result(xdata, ydatas, xname, yname, labels, yrange=range(0, 100, 10), log=False):
    fig = plt.figure()
    ls = len(labels)
    for i in range(ls):
        if log:
            plt.semilogy(range(len(xdata)), ydatas[i], color=colors[i],
                         inewidth=3.2, linestyle=line[i], marker=marker_style[i], ms=marksize, label=labels[i])
        else:
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
    # fig = gcf()
    # # 800 * 613
    fig.set_size_inches(size[0], size[1])
    canvas = FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)
    return response