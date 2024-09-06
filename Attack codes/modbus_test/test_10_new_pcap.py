# Script for changing the length

from scapy.all import *
from scapy.layers.inet import IP, TCP

file_input = "Modbus_VJTI_2k.pcapng"  # Input pcap file
file_output = "output1.pcapng"  # Output pcap file

# Read packets from the input file
packets = rdpcap(file_input)

pkts= packets[0:10]


# source_ip = "172.16.0.20"  
source_ip = "172.16.0.79"  


for packet in packets:
    if packet.haslayer(IP) and packet[IP].src == source_ip:
        # Get the raw bytes of the packet
        raw_bytes = bytes(packet)
        
        
        # Modify the packet
        modified_bytes = raw_bytes[:55] + b'\x00\x08' + raw_bytes[57:] + b'\x00\x01' 
        
        # Reconstruct the packet from the modified bytes
        modified_packet = Raw(load=modified_bytes)
        
        # Update the packet in the list
        packet = modified_packet

# Save the modified packets to a new pcap file
    wrpcap(file_output, packet,append=True)

print("Done")
