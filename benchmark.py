#! /usr/bin/python3
import urllib3
import time
from bs4 import BeautifulSoup
from tabulate import tabulate

urls = ["https://www.premiumnet.de/", "http://www.golem.de/", "http://feedly.com/i/welcome", "https://www.facebook.com/"]
numberOfRequests = 5
loadJS = True
loadCSS = True
loadImages = True

http = urllib3.PoolManager()
urllib3.disable_warnings()
timings = list()


def runBenchmarks():
    for page in urls:
        print("\nRunning page ", page)
        for i in range(0, numberOfRequests):
            print(". ", end="", flush=True)
            getBaseHTML(page, i)


def getBaseHTML(url, requestNumber):
    resourceQueue = list()
    htmlFile = benchmarkBaseHTML(url, requestNumber)
    if htmlFile.status != 200:
        return

    html = BeautifulSoup(htmlFile.data, 'html.parser')

    if loadJS:
        jsLinks = getJSLinks(html)
        resourceQueue.append(jsLinks)

    if loadCSS:
        cssLinks = getCssLinks(html)
        resourceQueue.append(cssLinks)

    if loadImages:
        imageLinks = getImageLinks(html)
        resourceQueue.append(imageLinks)

    benchmarkQueue(resourceQueue, url, requestNumber)


def getJSLinks(html):
    for link in html.find_all('script'):
        return link.get('src')


def getCssLinks(html):
    for link in html.find_all('rel="stylesheet"'):  # TODO rel=stylesheet
        return link.get('src')


def getImageLinks(html):
    for link in html.find_all('img'):
        return link.get('src')


def benchmarkBaseHTML(url, requestNumber):
    start = startTimer()
    htmlFile = http.request('GET', url)
    elapsedTime = stopTimer(start)
    saveTiming(elapsedTime, url, requestNumber)

    return htmlFile


def benchmarkQueue(links, url, requestNumber):
    for link in links:
        if link is not None:
            start = startTimer()
            http.request('GET', url+link)
            elapsedTime = stopTimer(start)
            saveTiming(elapsedTime, url, requestNumber, link)


def startTimer():
    return time.time()


def stopTimer(startTime):
    endTime = time.time()
    delta = endTime - startTime
    return delta


def saveTiming(elapsedTime, url, requestNumber, link=False):
    timing = [url, requestNumber, elapsedTime, link]
    timings.append(timing)


def printResults():
    print(tabulate(timings))


def analyzeTimings():
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

    return result


if __name__ == "__main__":
    # execute only if run as a script
    runBenchmarks()
    result = analyzeTimings()
    print("\n", result)
    printResults()
