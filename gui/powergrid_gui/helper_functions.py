import subprocess
import os

def run_flood_attack():
    # from attacks import synflood
    print("flood attack")

def run_mitm_attack():
    # from attacks import mitm
    print("mitm attack")

def start_client():
  print("starting client")
  os.system('sudo ./client/client.exe')

def start_server():
  print("starting server")
  os.system('sudo ./server/server.exe')


