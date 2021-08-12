# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from components.mainwindows import *
#import tkinter_Windows as tWin


if __name__ == '__main__':
    win = Window_tkinter()
    win.geometry('1580x980')
    ani = animation.FuncAnimation(f, animate_real_deal, interval=1400)
    print("tu sam stari moj dragi")
    win.mainloop()





