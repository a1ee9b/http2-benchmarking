#! /usr/bin/python3
import urllib3
from bs4 import BeautifulSoup

url = "https://www.premiumnet.de/"
numberOfRequests = 1
loadJS = True
loadCSS = True
loadImages = True

http = urllib3.PoolManager()
timings = list()


def runBenchmarks():
    for i in range(0, numberOfRequests):
        getBaseHTML(url, i)


def getBaseHTML(url, requestNumber):
    resourceQueue = list()
    htmlFile = benchmarkBaseHTML(url, requestNumber)
    # htmlFile = http.request('GET', url)
    print(htmlFile.status)
    if htmlFile.status != 200:
        return

    html = BeautifulSoup(htmlFile.data, 'html.parser')
    print(html.prettify)

    if loadJS:
        jsLinks = getJSLinks(html)
        resourceQueue.append(jsLinks)

    if loadCSS:
        cssLinks = getCssLinks(html)
        resourceQueue.append(cssLinks)

    if loadImages:
        imageLinks = getImageLinks(html)
        resourceQueue.append(imageLinks)

    print(resourceQueue)
    benchmarkQueue(resourceQueue, url, requestNumber)


def getJSLinks(html):
    for link in html.find_all('script'):
        return link.get('src')


def getCssLinks(html):
    for link in html.find_all('link'):  # TODO rel=stylesheet
        return link.get('src')


def getImageLinks(html):
    for link in html.find_all('img'):
        return link.get('src')


def benchmarkBaseHTML(url, requestNumber):
    startTimer()
    htmlFile = http.request('GET', url)
    stopTimer()
    saveTiming(url, requestNumber)

    return htmlFile


def benchmarkQueue(links, url, requestNumber):
    for link in links:
        if link is not None:
            startTimer()
            result = http.request('GET', url+link)
            print(result)
            stopTimer()
            saveTiming(url, requestNumber, link)


def startTimer():
    pass


def stopTimer():
    pass


def saveTiming(url, requestNumber, link=False):
    pass


if __name__ == "__main__":
    # execute only if run as a script
    runBenchmarks()
