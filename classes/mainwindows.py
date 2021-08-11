from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib
from classes.components.menubar import *
from classes.animate import *
import json

matplotlib.use('TkAgg')


class Window_tkinter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        print("tu")
        # tk.Tk.iconbitmap(self,default='@./mario.xbm')
        tk.Tk.wm_title(self, "Bot 'n' stuff")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = Menubar(container)
        tk.Tk.config(self, menu=menubar)

        self.__CreateJson()
        self.__CreateFrames(container)
        self.show_frame(GraphPage)

    # Create initial data if data doesnt exist
    def __CreateJson(self):
        dic = {"coin": "BTC", "fiat": "EUR", "oldcoin": "BTC", "iso8601start": "1531216800", "iso8601end": "1551648800"}
        with open("data.json", "w+") as jsonFile:
            json.dump(dic, jsonFile)

    def __CreateFrames(self, container):
        self.frames = {}

        for frame in (FirstPage, SettingsPage, GraphPage):
            newFrame = frame(container, self)
            self.frames[frame] = newFrame
            newFrame.grid(row=0, column=0, sticky='news')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label0 = tk.Label(self, text='Litecoin trading application', font=large_font)
        label0.pack(pady=25, padx=25)

        button0 = ttk.Button(self, text="Agree",
                             command=lambda: controller.show_frame(GraphPage))
        button0.pack()
        button02 = ttk.Button(self, text="Disagree",
                              command=lambda: quit())
        button02.pack()


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = tk.Label(self, text='Page One', font=large_font)
        label1.pack(pady=25, padx=25)
        # label11 = tk.Label(self, text='Description')
        # label11 .pack()

        button1 = ttk.Button(self, text="Confirm",
                             command=lambda: controller.show_frame(FirstPage))
        button2 = ttk.Button(self, text="Revert",
                             command=lambda: controller.show_frame(FirstPage))
        button1.pack()
        button2.pack()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Change coin:")
        label.pack()

        self.newcoin_var = tk.StringVar()
        market_name = ttk.Entry(self, textvariable=self.newcoin_var)
        market_name.pack()

        sub_btn = tk.Button(self, text='Submit', command=lambda: self.__ChangeCoing(controller))
        sub_btn.pack()

        button2 = tk.Button(self, text="goto First Page",
                            command=lambda: controller.show_frame(FirstPage))
        button2.pack()
        button3 = tk.Button(self, text="Options",
                            command=Options)
        button3.pack()

        self.__DrawGraph()



    def __ChangeCoing(self, controller):
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["oldcoin"] = data["coin"]
        data["coin"] = self.newcoin_var.get()

        with open("data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        controller.show_frame(GraphPage)

    def __DrawGraph(self):
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ani = animation.FuncAnimation(f, animate_real_deal, interval=1000)

