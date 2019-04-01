from scapy.all import *

import matplotlib.pyplot as plt

import argparse
import operator

from os import getuid

parser = argparse.ArgumentParser(description='Client/Server Live Traffic')

parser.add_argument('interface', help="Network interface to listen on i.e. en0", type=str)

parser.add_argument('--count', help="Capture X packets and exit", type=int)

args=parser.parse_args()

#Check to see if we are root, otherwise Scapy might not be able to listen

if getuid() != 0 :

   print("Warning: Not running as root, packet listening may not work.")

   try:

       print("--Trying to listen on {}".format(args.interface))

       sniff(iface=args.interface,count=1)

       print("--Success!")

   except:

       print("--Failed!\nError: Unable to sniff packets, try again using sudo.")

       quit()

if args.count:

   print("Capturing {} packets on interface {} ".format(args.count, args.interface))

else:

   print("Capturing unlimited packets on interface {} \n--Press CTRL-C to exit ".format(args.interface))

#Interactive Mode

plt.ion()

#Labels

plt.ylabel("Packets received")

plt.xlabel("Unit of Time")

plt.title("Real time Network Traffic")

plt.tight_layout()

#Empty to hold packets and their counts

srcCounts = {}
mostCommon = ''
maxCount = 0
seenIPs = []
yData=[]
yData1=[]
xData = []



i=0

#Listen indefinitely, or until we reach count

while True:

   #Listen for 1 packet

   for pkt in sniff(iface=args.interface,count=1):

       try:

           if IP  in pkt:

               if (str(pkt[IP].src)) in seenIPs:
                    #Get current value and add 1
                    count = srcCounts.get(str(pkt[IP].src))
                    count = count + 1
                    print(str(count))
                    srcCounts.update({str(pkt[IP].src) : count })
               else:
                    print('nope')
                    #Add to freq map
                    srcCounts.update({str(pkt[IP].src) : 1})
                    #Add to seen seenIPs
                    print(str(pkt[IP].src))
                    seenIPs.append(str(pkt[IP].src))
               # Get max of current source IP addresses
               yData.append(max(srcCounts.iteritems(), key=operator.itemgetter(1))[1])
               plt.plot(yData)

               #Pause and draw

               plt.pause(0.1)

               i+=1

               if args.count:

                   if i >= args.count:

                       quit()

       except KeyboardInterrupt:

           print("Captured {} packets on interface {} ".format(i, args.interface))

           quit()
