#!/usr/bin/env python3


import webbrowser
import os
import tempfile


_outputFilename = tempfile.gettempdir()+'/SignalFlowGraphGainSolverOutput.html'

_nodeStr = '{{id: {0}, label: "Node {0}", font: {{color: "black"}}}},\n'
_edgeStr = '{{from: {}, to: {}, label: "{}", arrows: "to", font: {{color: "black", align: "{}"}}}},\n'

_part1Str = ''
_part2Str = ''
_part3Str = ''
_part4Str = ''

_part1File = open('part1.txt')
_part2File = open('part2.txt')
_part3File = open('part3.txt')
_part4File = open('part4.txt')

for line in _part1File:
    _part1Str += line

for line in _part2File:
    _part2Str += line

for line in _part3File:
    _part3Str += line

for line in _part4File:
    _part4Str += line

_part1File.close()
_part2File.close()
_part3File.close()
_part4File.close()


def CreateJsHtmlFile (matrix, filename):
    n = len(matrix)

    nodes = '\n'
    for i in range(n):
        nodes += _nodeStr.format(str(i))

    edges = '\n'
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != '0':
                lengthyEnough = len(matrix[i][j]) > 2
                align = 'middle' if lengthyEnough else 'horizontal'
                edges += _edgeStr.format(str(i), str(j), matrix[i][j], align)

    part1StrFilled = _part1Str.format(os.getcwd())
    part3StrFilled = _part3Str.format(nodes, edges)
    sourceCode = part1StrFilled+_part2Str+part3StrFilled+_part4Str

    outputFile = open(filename, 'w')
    outputFile.write(sourceCode)


def OpenInWebBrowser (filename):
    webbrowser.get().open(filename)


def RenderSignalFlowGraph (matrix):
    CreateJsHtmlFile(matrix, _outputFilename)
    OpenInWebBrowser(_outputFilename)


if __name__ == '__main__':
    m = [ ['0', 'a', '0', '0'],
          ['sqrt(n)', '0', 'b', 'sigma'],
          ['d2', 'd1', '0', 'c'],
          ['0', '0', '0', 'phi'], ]
    CreateJsHtmlFile(m, _outputFilename)
    OpenInWebBrowser(_outputFilename)
