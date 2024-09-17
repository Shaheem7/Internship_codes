from scapy.all import *

file = "Modbus_VJTI_2k.pcapng"

packets = rdpcap(file)

pkts = packets[1:11]

pkt = pkts[0]


print(pkt.show())