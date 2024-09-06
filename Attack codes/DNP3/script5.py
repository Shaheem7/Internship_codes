from scapy.all import *
from scapy.layers.inet import TCP, IP

# Read packets from a pcap file
packets = rdpcap('Supervised_200.pcap')

PKT = packets[0]

print(PKT.summary())
print(PKT.show())