# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from classes.mainwindows import *
#import tkinter_Windows as tWin


if __name__ == '__main__':
    win = Window_tkinter()
    win.geometry("1280x720")
    win.maxsize(1920, 1080)
    win.minsize(640, 480)
    win.protocol("WM_DELETE_WINDOW", lambda : exit())
    win.mainloop()




