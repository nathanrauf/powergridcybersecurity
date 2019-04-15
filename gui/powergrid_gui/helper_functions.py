import subprocess
import os


def start_client(server_ip):
  print("Starting client")
  command = 'sudo ./client/client.exe ' + server_ip
  os.system(command)

def start_server():
  print("Starting server")
  os.system('sudo ./server/server.exe')

def start_packet_tracker(interface):
   print("Starting live packet viewer")
   command = 'python realTimeSniffer.py ' + interface
   os.system(command)







