# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/   

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    pullData = open("./graph_data/data.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

    
class PowerGridGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Power Grid Simulator")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        F = GraphPage
        frame = F(container, self)
        self.frames[F] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
# class StartPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self,parent)
#         label = tk.Label(self, text="Start Page", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button = ttk.Button(self, text="Visit Page 1",
#                             command=lambda: controller.show_frame(PageOne))
#         button.pack()

#         button2 = ttk.Button(self, text="Visit Page 2",
#                             command=lambda: controller.show_frame(PageTwo))
#         button2.pack()

#         button3 = ttk.Button(self, text="Graph Page",
#                             command=lambda: controller.show_frame(GraphPage))
#         button3.pack()


# class PageOne(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         button2 = ttk.Button(self, text="Page Two",
#                             command=lambda: controller.show_frame(PageTwo))
#         button2.pack()


# class PageTwo(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         button2 = ttk.Button(self, text="Page One",
#                             command=lambda: controller.show_frame(PageOne))
#         button2.pack()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # button1 = ttk.Button(self, text="Back to Home",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack()

        container_main = tk.Frame(self, background="#ffd3d3")
        container_graph_server = tk.Frame(self)
        container_graph_client = tk.Frame(self)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(in_=container_graph_server, side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(in_=container_graph_server, side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas2 = FigureCanvasTkAgg(f, self)
        canvas2.draw()
        canvas2.get_tk_widget().pack(in_=container_graph_client, side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar2 = NavigationToolbar2Tk(canvas2, self)
        toolbar2.update()
        canvas2._tkcanvas.pack(in_=container_graph_client, side=tk.TOP, fill=tk.BOTH, expand=True)

        container_graph_server.pack(in_=container_main, side="left")
        container_graph_client.pack(in_=container_main, side="left")
        container_main.pack(side="top", fill="x")



app = PowerGridGui()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()