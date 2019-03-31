import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

from pages.StartPage import *
from pages.PageOne import *
from pages.PageTwo import *
from pages.PageThree import *


def main():

  app = SeaofBTCapp()
  ani = animation.FuncAnimation(f, animate, interval=1000)
  app.mainloop()


def animate(i):
  f = Figure(figsize=(5,5), dpi=100)
  a = f.add_subplot(111)
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

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

if __name__ == '__main__':
    main()