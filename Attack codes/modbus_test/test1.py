from scapy.all import *
from scapy.layers.l2 import Ether

file = "2024_02_20_CII_Lab_Modbus.pcapng"
packets = rdpcap(file)	

print("Number of packets: ", len(packets))
print("First packet: ", packets[0])


for packet in packets:
    if packet.haslayer(Ether):
        print("TCP packet: ", packet.summary())

print("Packet summary: ", packet.summary())
print("Packet details: ", packet.show())
