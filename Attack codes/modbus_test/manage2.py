from scapy.all import *
from scapy.layers.inet import IP, TCP
from time import time



file1 = "modbus_12.pcapng"
file2 = "test_7.pcapng"

# Read packets from both files
packets1 = rdpcap(file1)
packets2 = rdpcap(file2)

# Set sequence numbers for the first two packets in packets2
if len(packets2) > 0 and packets2[0].haslayer(TCP):
    packets2[0][TCP].seq = 26
    del packets2[0][TCP].chksum  # Remove old checksum
if len(packets2) > 1 and packets2[1].haslayer(TCP):
    packets2[1][TCP].seq = 27
    del packets2[1][TCP].chksum  # Remove old checksum

# Rebuild the packets to update checksum
for packet in packets2:
    if packet.haslayer(TCP):
        packet[TCP].chksum = None  # Clear the checksum
        packet[IP].len = None      # Clear the IP length

# Combine the packets
packets3 = packets1 + packets2

# Write the combined packets to a new pcap file
new_file = "test733.pcapng"
wrpcap(new_file, packets3)

print("Done")
