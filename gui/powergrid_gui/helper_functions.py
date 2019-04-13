import subprocess
import os

def run_flood_attack():
    # from attacks import synflood
    print("flood attack")

def run_mitm_attack():
    # from attacks import mitm
    print("mitm attack")

def start_client(server_ip):
  print("starting client")
  command = 'sudo ./client/client.exe '  + server_ip
  os.system(command)

def start_server():
  print("starting server")
  os.system('sudo ./server/server.exe')


