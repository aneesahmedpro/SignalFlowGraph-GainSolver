#!/usr/bin/env python3


import tkinter as tk

from graphSolveGain import SolveFinalGain
from graphRender import RenderSignalFlowGraph


maxNoOfNodes = 20


class App (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.grid(sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frameMatrix = tk.Frame(self)
        frameControls = tk.Frame(self)

        frameMatrix.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=10, pady=10)
        for i in range(0, maxNoOfNodes+1):
            frameMatrix.grid_rowconfigure(i, weight=1)
            frameMatrix.grid_columnconfigure(i, weight=1)

        frameControls.grid(row=0, column=1, sticky='ns', padx=10, pady=10)

        self.noOfNodesStr = tk.StringVar()
        options = [str(i)+' Nodes' for i in range(1, maxNoOfNodes+1)]
        self.optionMenu = tk.OptionMenu(frameControls, self.noOfNodesStr, *options, command=self.UpdateMatrix)
        self.noOfNodesStr.set('Click here to select\n the Number of Nodes')
        self.optionMenu.grid(sticky='ew')

        tk.Label(frameControls).grid(pady=10)

        self.buttonDraw = tk.Button(frameControls, text='Draw', command=self.DrawGraph)
        self.buttonSolve = tk.Button(frameControls, text='Solve', command=self.SolveGraph)
        self.buttonHelp = tk.Button(frameControls, text='Help', command=self.ShowHelp)

        self.buttonDraw.grid(sticky='ew')
        self.buttonSolve.grid(sticky='ew')
        self.buttonHelp.grid(sticky='ew')

        self.rowLabels = []
        self.columnLabels = []
        for i in range(maxNoOfNodes):
            self.rowLabels.append(tk.Label(frameMatrix, text=str(i), relief=tk.SUNKEN, width=3))
            self.rowLabels[i].grid(row=i+1, column=0, sticky='nsew', padx=4, pady=4)
            self.rowLabels[i].grid_remove()
            self.columnLabels.append(tk.Label(frameMatrix, text=str(i), relief=tk.SUNKEN, width=3))
            self.columnLabels[i].grid(row=0, column=i+1, sticky='nsew', padx=4, pady=4)
            self.columnLabels[i].grid_remove()

        self.textBoxes = []
        for i in range(maxNoOfNodes):
            self.textBoxes.append([])
            for j in range(maxNoOfNodes):
                self.textBoxes[i].append(tk.Entry(frameMatrix, width=3))
                self.textBoxes[i][j].grid(row=i+1, column=j+1, sticky='nsew', padx=4, pady=4)
                self.textBoxes[i][j].grid_remove()
                self.textBoxes[i][j].bind('<FocusIn>', self.HighlightNodes)
                self.textBoxes[i][j].bind('<FocusOut>', self.UnhighlightNodes)

        self.defaultBgColour = self.rowLabels[0].config()['background'][4]

    def UpdateMatrix (self, value):
        self.noOfNodes = int(value.split()[0])

        for i in range(maxNoOfNodes):
            if i < self.noOfNodes:
                self.rowLabels[i].grid()
                self.columnLabels[i].grid()
            else:
                self.rowLabels[i].grid_remove()
                self.columnLabels[i].grid_remove()

        for i in range(maxNoOfNodes):
            for j in range(maxNoOfNodes):
                if i < self.noOfNodes and j < self.noOfNodes:
                    self.textBoxes[i][j].grid()
                else:
                    self.textBoxes[i][j].grid_remove()

    def HighlightNodes (self, event):
        for i in range(self.noOfNodes):
            for j in range(self.noOfNodes):
                if self.textBoxes[i][j] == event.widget:
                    self.rowLabels[i].config(bg='yellow')
                    self.columnLabels[j].config(bg='yellow')

    def UnhighlightNodes (self, event):
        for i in range(self.noOfNodes):
            for j in range(self.noOfNodes):
                if self.textBoxes[i][j] == event.widget:
                    self.rowLabels[i].config(bg=self.defaultBgColour)
                    self.columnLabels[j].config(bg=self.defaultBgColour)

    def ExtractMatrix (self):
        matrix = []
        for i in range(self.noOfNodes):
            matrix.append([])
            for j in range(self.noOfNodes):
                matrix[i].append(self.textBoxes[i][j].get())
        return matrix

    def PreprocessMatrix (self, matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == '':
                    matrix[i][j] = '0'
        return matrix

    def DrawGraph (self):
        matrix = self.ExtractMatrix()
        matrix = self.PreprocessMatrix(matrix)
        RenderSignalFlowGraph(matrix)

    def SolveGraph (self):
        matrix = self.ExtractMatrix()
        matrix = self.PreprocessMatrix(matrix)
        resultRaw, resultPretty = SolveFinalGain(matrix)
        print(resultPretty)

    def ShowHelp (self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('+600+300')
    root.grid()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    app = App(root)
    root.mainloop()
