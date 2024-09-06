from scapy.all import *

file = "ABB1.pcap"

packets = rdpcap(file)

pkts= packets[0:200] + packets[100:120] + packets[200:250] + packets[50:52] + packets[250: 300]


wrpcap("mms_replay.pcapng", pkts)