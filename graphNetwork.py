#!/usr/bin/env python3
from scapy.all import *
from collections import Counter
#from prettytable import PrettyTable
import plotly
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

#Read packet data from PCap file
packets = rdpcap('example.pcap')

#Read each packet to get data to add to list
srcIP = []

for pkt in packets:
	# if IP in packets:
	# 	print("hello")
		try:
			srcIP.append(pkt[IP].src)
		#Skip if packet doesnt have ip (retransmits, etc)
		except:
			pass

# for pkt in packets:
# 		if pkt.haslayer(DNSRR):
# 			if isinstance(pkt.an, DNSRR):
# 					print(pkt.an.rrname)

#BEGIN counting
cnt=Counter()

#Create ip list with corresponding frequencies
for ip in srcIP:
	cnt[ip] += 1

xData=[]
yData=[]

#######************ Psrt 1 - Table
#Create the table and header
# table= PrettyTable(["IP", "Count"])

# #Add data to table
# for ip, count in cnt.most_common():
# 	table.add_row([ip, count])

#######************ Psrt 2 - Bar Chart
for ip, count in cnt.most_common():
		xData.append(ip)
		yData.append(count)

#Create graph
plotly.offline.plot({"data":[ plotly.graph_objs.Bar( x=xData, y=yData) ], "layout":plotly.graph_objs.Layout(title="Source IP Frequency",xaxis=dict(title="Src IP"), yaxis=dict(title="count"))}, image='png')


#print table
#print(table)
