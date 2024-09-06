from scapy.all import *


file = "Supervised_200.pcap"

packets = rdpcap(file)


pkts = packets[:100] + packets[20:40] + packets[100:]

wrpcap("dnp3_replay.pcapng", pkts)

print("Done")