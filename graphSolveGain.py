#!/usr/bin/env python3


import sympy as sp


def SolveAllGains (matrix):
    n = len(matrix)
    matrix = sp.Matrix(matrix)
    identityMatrix = sp.eye(n)
    return (identityMatrix-matrix).inv()


def SolveFinalGain (matrix):
    n = len(matrix)
    finalGain = SolveAllGains(matrix)[0, n-1]
    return finalGain, sp.pretty(finalGain, use_unicode=True)


if __name__ == '__main__':
    m = [ ['0', 'a', '0', '0'],
          ['0', '0', 'b', '0'],
          ['0', 'd', '0', 'c'],
          ['0', '0', '0', '0'], ]
    print(SolveFinalGain(m)[1])
