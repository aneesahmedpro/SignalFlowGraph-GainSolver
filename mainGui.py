#!/usr/bin/env python3


import tkinter as tk
import tkinter.font as tkFont

from graphSolveGain import SolveFinalGain
from graphRender import RenderSignalFlowGraph


maxNoOfNodes = 20

screenWidth = 0
screenHeight = 0


class App (tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)

        self.root = root

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

        self.monoFont = tkFont.Font(self, font='monospace')

        self.update_idletasks()
        CenterifyWindow(self.root)

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

        self.update_idletasks()
        CenterifyWindow(self.root)

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
        self.ShowSolved(resultRaw, resultPretty)

    def ShowSolved (self, resultRaw, resultPretty):
        popup = tk.Toplevel(self)
        popup.title('Final Gain')
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_rowconfigure(1, weight=1)

        labelRaw = tk.Label(popup, text=resultRaw, bg='white', font=self.monoFont)
        labelPretty = tk.Label(popup, text=resultPretty, bg='white', font=self.monoFont)

        labelRaw.grid(sticky='ew', padx=10, pady=10)
        labelPretty.grid(sticky='ew', padx=10, pady=10)

        popup.update_idletasks()
        width, height, posX, posY = ParseWindowGeometry(popup.geometry())
        if width < 200:
            width = 200
        if height < 150:
            height = 150
        posX = (screenWidth-width)//2
        posY = (screenHeight-height)//2
        popup.geometry('{}x{}+{}+{}'.format(width, height, posX, posY))

        popup.focus()
        popup.grab_set()
        self.wait_window(popup)

    def ShowHelp (self):
        pass


def ParseWindowGeometry (string):
    temp1 = string.split('+')
    temp2 = temp1[0].split('x')
    return int(temp2[0]), int(temp2[1]), int(temp1[1]), int(temp1[2]) # W,H,X,Y

def CenterifyWindow (toplevelWindow):
    width, height, posX, posY = ParseWindowGeometry(toplevelWindow.geometry())
    posX = (screenWidth-width)//2
    posY = (screenHeight-height)//2
    toplevelWindow.geometry('+{}+{}'.format(posX, posY))


if __name__ == '__main__':
    root = tk.Tk()
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    root.grid()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    app = App(root)
    root.mainloop()
