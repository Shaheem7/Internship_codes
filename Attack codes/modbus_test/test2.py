from scapy.all import *
from scapy.layers.inet import IP, TCP
from time import time


file1 = "modbus_12.pcapng"
file2 = "test_7.pcapng"

# Read packets from both files
packets1 = rdpcap(file1)
packets2 = rdpcap(file2)

# Assuming packets1 is the original session
# Find the last sequence number and timestamp in packets1
last_seq = packets1[-1][TCP].seq if packets1[-1].haslayer(TCP) else 0
last_time = packets1[-1].time if packets1[-1].haslayer(TCP) else 0

# Adjust packets2
for packet in packets2:
    if packet.haslayer(TCP):
        packet[TCP].seq = 26
        packet.time = last_time + (packet.time - packets2[0].time)

        # Recalculate checksums and lengths
        del packet[TCP].chksum  # Remove the old TCP checksum
        del packet[IP].len      # Remove the old IP length
        del packet[IP].chksum   # Remove the old IP checksum

        # Rebuild the packet to update checksums and lengths
        packet = packet.__class__(bytes(packet))

# Combine the packets
packets3 = packets1 + packets2

# Write the combined packets to a new pcap file
new_file = "test7111.pcapng"
wrpcap(new_file, packets3)

print("Done")
