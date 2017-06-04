#!/usr/bin/env python3


import webbrowser
import os


_part1Str = ''
_part2Str = ''
_part3Str = ''

_part1File = open('part1.txt')
_part2File = open('part2.txt')
_part3File = open('part3.txt')

while True:
    line = _part1File.readline()
    if line == '':
        break
    _part1Str += line

while True:
    line = _part2File.readline()
    if line == '':
        break
    _part2Str += line

while True:
    line = _part3File.readline()
    if line == '':
        break
    _part3Str += line

_part1File.close()
_part2File.close()
_part3File.close()


def CreateJsHtmlFile (matrix, filename):
    n = len(matrix)

    nodes = '\n'
    for i in range(n):
        nodes += '{id: '+str(i)+', label: \'Node '+str(i)+'\'},\n'

    edges = '\n'
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != '0':
                edges += '{from: '+str(i)+', to: '+str(j)+', label: \''\
                         +matrix[i][j]+'\', arrows:\'to\', font: {align: \'top\'}},\n'

    sourceCode = _part1Str+nodes+_part2Str+edges+_part3Str

    outputFile = open(filename, 'w')
    outputFile.write(sourceCode)


def OpenInWebBrowser (filename):
    webbrowser.get().open(filename)


def RenderSignalFlowGraph (matrix):
    CreateJsHtmlFile(matrix, 'temp.html')
    OpenInWebBrowser('temp.html')


if __name__ == '__main__':
    CreateJsHtmlFile([['0', 'a', '0', '0'], ['0', '0', 'b', '0'], ['0', 'd', '0', 'c'], ['0', '0', '0', '0']], 'temp.html')
    OpenInWebBrowser('temp.html')
