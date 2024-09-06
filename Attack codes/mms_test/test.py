from scapy.all import *


file = "ABB1.pcap"

packets = rdpcap(file)

pkt = packets[3]

pkt_bytes = bytes(pkt)

print(pkt_bytes)


# change a specific byte
pkt_bytes = pkt_bytes[:-12] + b'\x09' + pkt_bytes[-11:]

print(pkt_bytes)

wrpcap("ABB1_modified.pcap", pkt_bytes)