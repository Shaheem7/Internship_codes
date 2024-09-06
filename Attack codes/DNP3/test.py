from scapy.all import *

# Load packets from a pcap file
packets = rdpcap('Supervised_200.pcap')

pkt = packets[2]

bytess = bytes(pkt)

print(bytess)

Bytes = b'\x12\x99\x00?\x1a[\x05d\x0b\xc4\x0c\x00\x01\x00.\xc5\xc3\xc0\x01<\x02\x06\x04s'
# Replay packets
# for packet in packets:
#     sendp(packet, verbose=0)  # sendp for Ethernet frames, use send for IP packets

