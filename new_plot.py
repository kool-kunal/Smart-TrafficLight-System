from cProfile import label
import os
import json
from math import pi
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib


def doughnut_plot(key, data):
    font = {'family': 'normal',
            'size': 16}

    matplotlib.rc('font', **font)
    fig, ax = plt.subplots(figsize=((6,6)))
    ax = plt.subplot()

    startangle = 90
    colors = ['#4393E5', '#43BAE5', '#7AE6EA', '#7AE6EA']

    # xs = [(i * pi * 2) for (d, i) in data]
    # d = -0.2
    # ys = []
    # for i in range(len(xs)):
    #     ys.append(d)
    #     d += 1.2
    size = 0.2
    #left = (startangle * pi * 2)
    for i in data:
        # ax.barh(ys[i], x, left=left, height=1,
        #         color=colors[i], label=data[i][1])
        # ax.scatter(x+left, ys[i], s=350, color=colors[i], zorder=2)
        # ax.scatter(left, ys[i], s=350, color=colors[i], zorder=2)
        wedges, texts = ax.pie([i[1], 1-i[1]], radius=size, colors=[colors[0],
               colors[1]], wedgeprops=dict(width=0.15, edgecolor='b'), )
        size += 0.2

        bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                bbox=bbox_props, zorder=0, va="center")

        for j, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            t = 'TTLS(GLT=' + i[0]+')' if j==1 else 'Net'
            ax.annotate(t, xy=(x, y), xytext=(1.2*np.sign(x), 1.2*y),
                        horizontalalignment=horizontalalignment, **kw)
        #ax.set(aspect="equal", title='Pie plot with `ax.pie`')

    # plt.ylim(-4, 4)
    # # legend
    # legend_elements = []

    # z = 0
    # for d, i in data:
    #     legend_elements.append(Line2D(
    #         [0], [0], marker='o', color='w', label="Cars="+d, markerfacecolor=colors[z], markersize=10))
    #     z += 1
    # ax.legend(handles=legend_elements, loc='center', frameon=False)
    # plt.title('Test Results\nSingle Intersection\nagainst TTLS with G.L.T =' +
    #           key, fontsize=16, loc='center')

    # plt.xticks([])
    # plt.yticks([])
    # ax.spines.clear()
    # plt.savefig(os.path.join(os.getcwd(), f'{key}.png'))

    plt.show()


folder_path = "/home/kunal/Desktop/college/major_project/Smart-TrafficLight-System/test_results"

data = {"15": [], "30": [], "60": [], "120": []}

for fol in os.listdir(folder_path):
    result_path = os.path.join(folder_path, fol + "/test_results.json")
    with open(result_path, 'r') as f:
        result = json.load(f)
        net = [result[test]["net"]
               ["HARMONIC_MEAN_LOSS"] for test in result]
        ttl = [result[test]["ttl"]
               ["HARMONIC_MEAN_LOSS"] for test in result]

        count = 0
        for _ in range(len(net)):
            if net[_] <= ttl[_]:
                count += 1
        #print(fol, count, len(net))
        data[fol.split("_")[-1]].append((fol.split("_")[1], count/len(net)))

# print(data)
for k, d in data.items():
    d.sort(key=lambda x: int(x[0]))
    doughnut_plot(k, d)
