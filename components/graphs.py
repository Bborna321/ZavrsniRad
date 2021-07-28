import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("TkAgg")
from tkinter import ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Graphs:
    def __init__(self, MACDline, signalLine):
        root = tk.Tk()

        canvas1 = tk.Canvas(root, width = 800, height = 300)
        canvas1.pack()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        root.mainloop()


    def MovingAverageMACD(self, MACDline, signalLine):
        MACDline = self.__DenseSet(MACDline, 100)
        signalLine = self.__DenseSet(signalLine, 100)
        x = np.array(range(len(MACDline)))


        plt.plot(x, MACDline)
        plt.plot(x, signalLine)
        idx = np.argwhere(np.diff(np.sign(MACDline - signalLine))).flatten()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a = plt.plot(x[idx], MACDline[idx], 'ro')
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.both,expand = True)


    def __DenseSet(self, set, numElements):
            set = np.array(set)
            temp = np.array([])
            for i in range(0, set.shape[0]):
                x = np.linspace(set[i-1], set[i], num = numElements)
                x = x[0 : -1]
                temp = np.concatenate((temp, x))
            return temp
