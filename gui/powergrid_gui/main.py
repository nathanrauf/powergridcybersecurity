# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/
import tkinter as tk
from tkinter import ttk
from scapy.all import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import os
from helper_functions import start_client, start_server
import re
from Mitm import *
from SynFlood import *
from os import getuid
import operator


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

        self.shared_data = {
            "client_ip": tk.StringVar(),
            "router_ip": tk.StringVar(),
            "interface": tk.StringVar(),
            "port": tk.StringVar(),
        }


        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Power Grid Simulator")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ClientServerUserInput, ClientPage, ServerPage, GraphPage, LivePlot):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        label = tk.Label(self, text="Power Grid Management System", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        client_button = ttk.Button(self, text="Start Client (Substation)",
                            command=lambda: controller.show_frame(ClientPage))
        client_button.pack()

        server_button = ttk.Button(self, text="Start Server (Control Center)",
                            command=lambda: controller.show_frame(ServerPage))
        server_button.pack()

        user_input_page = ttk.Button(self, text="Attacker Dashboard",
                            command=lambda: controller.show_frame(ClientServerUserInput))
        user_input_page.pack()

        live_plot_button = ttk.Button(self, text="View Packets",
                            command=lambda: controller.show_frame(LivePlot))
        live_plot_button.pack()


class LivePlot(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()

        labelText=tk.StringVar()
        labelText.set("Enter interface name to listen:")
        labelDir=tk.Label(self, textvariable=labelText,height=2)
        labelDir.pack()

        interface=tk.StringVar(None)
        self.interfacename=tk.Entry(self,textvariable=interface,width=20)
        self.interfacename.pack()

        buttonCommit = ttk.Button(self, text="Submit",
                            command=lambda: self.launchPlot(controller))
        buttonCommit.pack()


    def launchPlot(self,controller):
        if getuid() != 0:
            print ("Run with sudo")
            try:
                sniff(iface=self.interfacename.get(),count=1)
            except:
                print("Error")
                quit()

        plt.ion()
        plt.ylabel("Packets received")

        plt.xlabel("Unit of Time")

        plt.title("Real time Network Traffic")

        plt.tight_layout()

        srcCounts = {}
        mostCommon = ''
        maxCount = 0
        seenIPs = []
        yData=[]
        yData1=[]
        xData = []
        i=0
        count = 200

        while True:
             for pkt in sniff(iface=self.interfacename.get(),count=1):

                 try:

                     if IP  in pkt:

                         if (str(pkt[IP].src)) in seenIPs:
                              #Get current value and add 1
                              count = srcCounts.get(str(pkt[IP].src))
                              count = count + 1
                              srcCounts.update({str(pkt[IP].src) : count })
                         else:
                              #Add to freq map
                              srcCounts.update({str(pkt[IP].src) : 1})
                              #Add to seen seenIPs
                              print(str(pkt[IP].src))
                              seenIPs.append(str(pkt[IP].src))
                         # Get max of current source IP addresses
                         yData.append(max(srcCounts.items(), key=operator.itemgetter(1))[1])
                         plt.plot(yData)

                         #Pause and draw

                         plt.pause(0.1)

                         i+=1

                         # if args.count:
                         #
                         #     if i >= args.count:
                         #
                         #         quit()

                 except KeyboardInterrupt:

                     print("Captured {} packets on interface {} ".format(i, self.interfacename.get()))

                     quit()

        # text_box_client = tk.Text(self, height=2, width=20)
        # text_box_client.pack()
        #
        #
        # self.client_ip_input = text_box_client




class ClientPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Substation Controller", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        start_client_button = ttk.Button(self, text="Start client",
                            command=lambda: start_client("196.128.86.1"))
        start_client_button.pack()


        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()


class ServerPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Control Center", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        start_server_button = ttk.Button(self, text="Start server",
                                command=lambda: start_server())
        start_server_button.pack()

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()


class ClientServerUserInput(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        client_frame = tk.Frame(self)
        server_frame = tk.Frame(self)
        interface_frame = tk.Frame(self)
        port_frame = tk.Frame(self)

        # text_box_client = ttk.Entry(self, height=2, width=10)
        label_client = tk.Label(self, text="Victim IP Address")
        label_client.pack(in_=client_frame, side="left")
        label_server = tk.Label(self, text="Router IP Address")
        label_server.pack(in_=server_frame, side="left")
        label_interface = tk.Label(self, text="Interface")
        label_interface.pack(in_=interface_frame, side="left")
        label_port = tk.Label(self, text="Port Number")
        label_port.pack(in_=port_frame, side="left")

        text_box_client = ttk.Entry(self, textvariable=self.controller.shared_data["client_ip"])
        text_box_client.pack(in_=client_frame, side="right")

        text_box_server = ttk.Entry(self, textvariable=self.controller.shared_data["router_ip"])
        text_box_server.pack(in_=server_frame, side="right")

        text_box_interface = ttk.Entry(self, textvariable=self.controller.shared_data["interface"])
        text_box_interface.pack(in_=interface_frame, side="right")

        text_box_port = ttk.Entry(self, textvariable=self.controller.shared_data["port"])
        text_box_port.pack(in_=port_frame, side="right")

        self.client_ip_input = text_box_client
        self.router_ip_input = text_box_server

        buttonCommit = ttk.Button(self, text="Submit",
                            command=lambda: self.retrieve_input(controller))
        buttonCommit.pack()

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()

        client_frame.pack(side="top", fill="x")
        server_frame.pack(side="top", fill="x")
        interface_frame.pack(side="top", fill="x")
        port_frame.pack(side="top", fill="x")


    def retrieve_input(self,controller):

        client_ip = self.client_ip_input.get()
        router_ip = self.router_ip_input.get()

        ip_regex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

        if ip_regex.match(client_ip) and ip_regex.match(router_ip):
            controller.show_frame(GraphPage)
        else:
            # TODO: add error text
            print("Enter correct input")

        
class GraphPage(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller
        self.mitm_intstance = None
        self.synflood_instance = None

        tk.Frame.__init__(self, parent)


        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        floodBtn = ttk.Button(self, text="Initiate SYN Flood Attack", command=lambda: self.run_flood_attack())
        floodBtn.pack()

        mitmAttackBtn = ttk.Button(self, text="Initiate MITM Attack", command=lambda: self.run_mitm_attack())
        mitmAttackBtn.pack()

        stop_mitm_attack_btn = ttk.Button(self, text="Stop MITM Attack", command=lambda: self.stop_mitm_attack())
        stop_mitm_attack_btn.pack()

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()

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


    def run_flood_attack(self):
      # from attacks import synflood
        victim_ip = self.controller.shared_data["client_ip"].get()
        victim_port = self.controller.shared_data["port"].get()
        # Set as input
        num_packets = 10000

        self.synflood_instance = SynFlood(victim_ip, victim_port, num_packets)
        self.synflood_instance.start_attack()

    def run_mitm_attack(self):

        victim = self.controller.shared_data["client_ip"].get()
        router = self.controller.shared_data["router_ip"].get()
        interface = self.controller.shared_data["interface"].get()
        self.mitm_intstance = Mitm(interface, victim, router)
        self.mitm_intstance.start_attack()

    def stop_mitm_attack(self):
        self.mitm_intstance.stop_attack()


app = PowerGridGui()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
