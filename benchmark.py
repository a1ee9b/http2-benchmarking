#! /usr/bin/python3
# from hyper import HTTPConnection
import os

import requests
from hyper.contrib import HTTP20Adapter
import time
import csv
from bs4 import BeautifulSoup
from tabulate import tabulate

host = "localhost"
urls = [
    "http://"+host+":9001/unoptimized",
    "http://"+host+":9001/concatenated",
    "http://"+host+":9001/optimized",
    "http://"+host+":9001/requests100",
    "https://"+host+":9002/unoptimized",
    "https://"+host+":9002/concatenated",
    "https://"+host+":9002/optimized",
    "https://"+host+":9002/requests100",
    "https://"+host+":9003/unoptimized",
    "https://"+host+":9003/concatenated",
    "https://"+host+":9003/optimized",
    "https://"+host+":9003/requests100"
]

numberOfRequests = 1000
loadJS = True
loadCSS = True
loadImages = True

timestamp = str(time.strftime('%Y-%m-%d'))
filename = os.path.join('results', 'benchmark-lokal-'+str(numberOfRequests)+'-'+timestamp+'.csv')


requests.packages.urllib3.disable_warnings()
s = requests.Session()
s.mount('localhost', HTTP20Adapter())


def runBenchmarks(links):
    for page in links:
        print("\nRunning page ", page)
        timings = list()
        for i in range(0, numberOfRequests):
            print(".", end="", flush=True)
            runTiming = runBaseHTML(page, i)
            timings.extend(runTiming)

        analyzeTimings(timings)

        with open(filename, 'a+', newline = '') as csvFile:
            writer = csv.writer(csvFile, delimiter = ';', quotechar = '\\', quoting = csv.QUOTE_MINIMAL)
            for timing in timings:
                writer.writerow(timing)


def runBaseHTML(url, requestNumber):
    resourceQueue = list()
    (htmlFile, timing) = benchmarkBaseHTML(url, requestNumber)

    html = BeautifulSoup(htmlFile, 'html.parser')

    if loadJS:
        jsLinks = getJSLinks(html)
        if jsLinks is not None:
            resourceQueue.extend(jsLinks)

    if loadCSS:
        cssLinks = getCssLinks(html)
        if cssLinks is not None:
            resourceQueue.extend(cssLinks)

    if loadImages:
        imageLinks = getImageLinks(html)
        if imageLinks is not None:
            resourceQueue.extend(imageLinks)

    timings = benchmarkQueue(resourceQueue, url, requestNumber)
    timings.append(timing)
    return timings


def getJSLinks(html):
    allPaths = list()
    allLinks = html.find_all('script')
    for link in allLinks:
        allPaths.append(link.get('src'))

    return allPaths


def getCssLinks(html):
    allPaths = list()
    allLinks = html.find_all('link')
    for link in allLinks:
        allPaths.append(link.get('href'))

    return allPaths


def getImageLinks(html):
    for link in html.find_all('img'):
        return link.get('src')


def benchmarkBaseHTML(url, requestNumber):
    start = startTimer()
    htmlFile = s.get(url, verify=False).text
    elapsedTime = stopTimer(start)

    return htmlFile, [url, requestNumber, elapsedTime, False]


def benchmarkQueue(links, url, requestNumber):
    timings = list()
    for link in links:
        if link is not None:
            start = startTimer()

            s.get(url+link, verify = False)

            elapsedTime = stopTimer(start)
            timings.append([url, requestNumber, elapsedTime, link])

    return timings


def startTimer():
    return time.time()


def stopTimer(startTime):
    endTime = time.time()
    delta = endTime - startTime
    return delta


def printResults(timings):
    print(tabulate(timings))


def analyzeTimings(timings):
    minimum = 100
    minimumRequest = None
    maximum = 0
    maximumRequest = None
    totalBase = 0
    totalResources = 0

    for timing in timings:
        if timing[3] is not False:
            totalResources += timing[2]
        else:
            totalBase += timing[2]

        if timing[2] < minimum:
            minimum = timing[2]
            minimumRequest = timing

        if timing[2] > maximum:
            maximum = timing[2]
            maximumRequest = timing

    total = totalBase + totalResources
    mean = total / numberOfRequests

    result = {'total': total,
              'mean': mean,
              'minimum': minimum,
              'minimumRequest': minimumRequest,
              'maximum': maximum,
              'maximumRequest': maximumRequest,
              'totalBase': totalBase,
              'totalResources': totalResources}

    print(result)

    return result


if __name__ == "__main__":
    runBenchmarks(urls)
    # printResults()
