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
import subprocess 
import signal
from helper_functions import start_client, start_server, start_packet_tracker
import re
from SynFlood import *
from os import getuid
import operator


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")


class PowerGridGui(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {
            "client_ip": tk.StringVar(),
            "server_ip": tk.StringVar(),
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

        for F in (StartPage, ClientServerUserInput, ClientPage, ServerPage, AttackerDashboard, LivePlot):
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

        labelText=tk.StringVar()
        labelText.set("Enter interface name to listen:")
        labelDir=tk.Label(self, textvariable=labelText,height=2)
        labelDir.pack()

        interface=tk.StringVar(None)
        self.interfacename=tk.Entry(self,textvariable=interface,width=20)
        self.interfacename.pack()

        buttonCommit = ttk.Button(self, text="Submit",
                            command=lambda: start_packet_tracker(self.interfacename.get()))
        buttonCommit.pack()

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()

class ClientPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Substation Controller", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        labelText=tk.StringVar()
        labelText.set("Enter server IP:")
        labelDir=tk.Label(self, textvariable=labelText,height=2)
        labelDir.pack()

        server=tk.StringVar(None)
        self.server_ip=tk.Entry(self,textvariable=server,width=20)
        self.server_ip.pack()

        pass_label_text=tk.StringVar()
        pass_label_text.set("Enter client password:")
        pass_label_dir=tk.Label(self, textvariable=pass_label_text,height=2)
        pass_label_dir.pack()

        passw=tk.StringVar(None)
        self.client_pass=tk.Entry(self,show='*',width=20)
        self.client_pass.pack()

        start_client_button = ttk.Button(self, text="Start client",
                            command=lambda: start_client(self.server_ip.get(), self.client_pass.get()))
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

        text_box_server = ttk.Entry(self, textvariable=self.controller.shared_data["server_ip"])
        text_box_server.pack(in_=server_frame, side="right")

        text_box_interface = ttk.Entry(self, textvariable=self.controller.shared_data["interface"])
        text_box_interface.pack(in_=interface_frame, side="right")

        text_box_port = ttk.Entry(self, textvariable=self.controller.shared_data["port"])
        text_box_port.pack(in_=port_frame, side="right")

        self.client_ip_input = text_box_client
        self.router_ip_input = text_box_server

        client_frame.pack(side="top", fill="x")
        server_frame.pack(side="top", fill="x")
        interface_frame.pack(side="top", fill="x")
        port_frame.pack(side="top", fill="x")


        buttonCommit = ttk.Button(self, text="Submit",
                            command=lambda: self.retrieve_input(controller))
        buttonCommit.pack()

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()

    def retrieve_input(self,controller):

        client_ip = self.client_ip_input.get()
        router_ip = self.router_ip_input.get()

        ip_regex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

        if ip_regex.match(client_ip) and ip_regex.match(router_ip):
            controller.show_frame(AttackerDashboard)
        else:
            # TODO: add error text
            print("Enter correct input")

        
class AttackerDashboard(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller
        self.mitm_intstance = None
        self.synflood_instance = None

        tk.Frame.__init__(self, parent)


        label = tk.Label(self, text="Attacker Dashboard", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        floodBtn = ttk.Button(self, text="Initiate SYN Flood Attack", command=lambda: self.run_flood_attack())
        floodBtn.pack()

        mitmAttackBtn = ttk.Button(self, text="Initiate MITM Attack", command=lambda: self.start_mitm_attack(self.get_input_interface(), self.get_input_client_ip(), self.get_input_server_ip()))
        mitmAttackBtn.pack()

        stop_mitm_attack_btn = ttk.Button(self, text="Stop MITM Attack", command=lambda: self.stop_mitm_attack())
        stop_mitm_attack_btn.pack()

        back_to_origin = ttk.Button(self, text="Back to Origin",
                            command=lambda: controller.show_frame(StartPage))
        back_to_origin.pack()

    def run_flood_attack(self):
      # from attacks import synflood
        victim_ip = self.controller.shared_data["client_ip"].get()
        victim_port = self.controller.shared_data["port"].get()
        # Set as input
        num_packets = 10000

        self.synflood_instance = SynFlood(victim_ip, victim_port, num_packets)
        self.synflood_instance.start_attack()

    def get_input_client_ip(self):
        victim = self.controller.shared_data["client_ip"].get()
        return victim

    def get_input_server_ip(self):
        router = self.controller.shared_data["server_ip"].get()
        return router

    def get_input_interface(self):
        interface = self.controller.shared_data["interface"].get()
        return interface

    def start_mitm_attack(self, interface, victim_ip, gate_ip):
        print("Starting MITM attack")
        command = ['python', 'mitm.py', interface, victim_ip, gate_ip]
        self.mitm_intstance = subprocess.Popen(command)

    def stop_mitm_attack(self):
      os.kill(self.mitm_intstance.pid, signal.SIGINT)


app = PowerGridGui()
app.mainloop()
