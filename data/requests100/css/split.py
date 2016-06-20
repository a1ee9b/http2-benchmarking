#!/usr/local/bin/python

import math

filePath = './bootstrap.css'
filePattern = './bootstrap-{0}.css'
lineCount = 6761
line100th = math.floor(lineCount / 100)

with open(filePath) as file:
    splitNumber = 1
    splitContent = ""
    for i, l in enumerate(file):
        splitContent += l
        if i % line100th == 0:
            with open(filePattern.format(splitNumber), 'w+') as splitFile:
                splitFile.write(splitContent)
                splitContent = ""
                splitNumber += 1
