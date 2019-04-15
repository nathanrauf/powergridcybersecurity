import subprocess
import os


def start_client(server_ip):
  print("starting client")
  command = 'sudo ./client/client.exe ' + server_ip
  os.system(command)

def start_server():
  print("starting server")
  os.system('sudo ./server/server.exe')






