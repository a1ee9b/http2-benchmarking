#! /usr/bin/python3

## numpy is used for creating fake data
from collections import defaultdict
from enum import IntEnum
import csv
import os
import matplotlib as mpl

## agg backend is used to create plot as a .png file
mpl.use('agg')

import matplotlib.pyplot as plt


class Methods(IntEnum):
    http = 1
    ssl = 2
    http2 = 3


class Optimizations(IntEnum):
    unoptimized = 1
    concatenated = 2
    optimized = 3
    requests100 = 4


def main():
    lokal1000 = os.path.join('results', 'benchmark-lokal-1000-2016-07-11.csv')
    benchmarkData = readCSV(lokal1000)

    plotDrei(benchmarkData)
    plotVier(benchmarkData)


def plotDrei(benchmarkData):
    data_to_plot = [
        list(benchmarkData[Optimizations.unoptimized][Methods.http].values()),
        list(benchmarkData[Optimizations.unoptimized][Methods.ssl].values()),
        list(benchmarkData[Optimizations.unoptimized][Methods.http2].values()),
        list(benchmarkData[Optimizations.concatenated][Methods.http].values()),
        list(benchmarkData[Optimizations.concatenated][Methods.ssl].values()),
        list(benchmarkData[Optimizations.concatenated][Methods.http2].values()),
        list(benchmarkData[Optimizations.optimized][Methods.http].values()),
        list(benchmarkData[Optimizations.optimized][Methods.ssl].values()),
        list(benchmarkData[Optimizations.optimized][Methods.http2].values())
    ]
    legend = [
        "unoptimized - http",
        "unoptimized - ssl",
        "unoptimized - http2",
        "concatenated - http",
        "concatenated - ssl",
        "concatenated - http2",
        "optimized - http",
        "optimized - ssl",
        "optimized - http2",
    ]

    plot(data_to_plot, legend, os.path.join('results','lokal_drei.png'))


def plotVier(benchmarkData):
    data_to_plot = [
        list(benchmarkData[Optimizations.requests100][Methods.http].values()),
        list(benchmarkData[Optimizations.requests100][Methods.ssl].values()),
        list(benchmarkData[Optimizations.requests100][Methods.http2].values()),
        list(benchmarkData[Optimizations.unoptimized][Methods.http].values()),
        list(benchmarkData[Optimizations.unoptimized][Methods.ssl].values()),
        list(benchmarkData[Optimizations.unoptimized][Methods.http2].values()),
        list(benchmarkData[Optimizations.concatenated][Methods.http].values()),
        list(benchmarkData[Optimizations.concatenated][Methods.ssl].values()),
        list(benchmarkData[Optimizations.concatenated][Methods.http2].values()),
        list(benchmarkData[Optimizations.optimized][Methods.http].values()),
        list(benchmarkData[Optimizations.optimized][Methods.ssl].values()),
        list(benchmarkData[Optimizations.optimized][Methods.http2].values())
    ]
    legend = [
        "requests100 - http",
        "requests100 - ssl",
        "requests100 - http2",
        "unoptimized - http",
        "unoptimized - ssl",
        "unoptimized - http2",
        "concatenated - http",
        "concatenated - ssl",
        "concatenated - http2",
        "optimized - http",
        "optimized - ssl",
        "optimized - http2",
    ]

    plot(data_to_plot, legend, os.path.join('results', 'lokal_vier.png'))


def plot(data, labels, filename):
    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    bp = ax.boxplot(data, patch_artist=True, showfliers=False, sym='')

    # change outline color, fill color and linewidth of the boxes
    boxNum = 1
    for box in bp['boxes']:
        # change outline color
        box.set(color='#161616', linewidth=2)
        # change fill color
        if boxNum % 3 is 1:
            box.set(facecolor='#37B63B')
        elif boxNum % 3 is 2:
            box.set(facecolor='#3CA2FD')
        else:
            box.set(facecolor='#FCE701')

        boxNum += 1

    # change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='#161616', linewidth=2)

    # change color and linewidth of the caps
    # for cap in bp['caps']:
    #     cap.set(color='#7570b3', linewidth=2)

    # change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='#161616', linewidth=2)

    # # change the style of fliers and their fill
    # for flier in bp['fliers']:
    #     flier.set(marker='o', color='#e7298a', alpha=0.5)

    # Custom x-axis labels
    ax.set_xticklabels(labels, rotation=90)

    # Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Save the figure
    fig.savefig(filename, bbox_inches='tight')

    plt.clf()


def readCSV(filename):
    result = dict()

    for optimization in Optimizations:
        result[optimization] = dict()
        for method in Methods:
            result[optimization][method] = defaultdict(float)

    with open(filename, 'r') as CSVfile:
        reader = csv.reader(CSVfile, delimiter=';', quotechar='/')
        for row in reader:
            url = row[0]
            requestNumber = int(row[1])
            timing = float(row[2])
            # isResource = True if row[3] is not "False" else False

            if "9001" in url:
                method = Methods.http
            elif "9002" in url:
                method = Methods.ssl
            else:
                method = Methods.http2

            if "unoptimized" in url:
                optimization = Optimizations.unoptimized
            elif "concatenated" in url:
                optimization = Optimizations.concatenated
            elif "optimized" in url:
                optimization = Optimizations.optimized
            else:
                optimization = Optimizations.requests100

            tempTiming = result[optimization][method][requestNumber] if result[optimization][method][requestNumber] is not None else 0.0
            result[optimization][method][requestNumber] = tempTiming + timing

    return result

if __name__ == "__main__":
    main()
