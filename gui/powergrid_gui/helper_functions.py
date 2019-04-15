import subprocess
import os


def start_client(server_ip, password):
  print("Starting client")
  command = ['sudo', './client/client.exe', server_ip, password]
  subprocess.Popen(command)

def start_server():
  print("Starting server")
  command = ['sudo', './server/server.exe']
  subprocess.Popen(command)

def start_packet_tracker(interface):
   print("Starting live packet viewer")
   command = ['python', 'realTimeSniffer.py', interface]
   subprocess.Popen(command)







