from scapy.all import *
import time
from scapy.layers.inet import TCP, IP 
from scapy.layers.l2 import Ether   

from scapy.all import *
import time

# Load the packet from a pcap file
packetss = rdpcap('Supervised_200.pcap')

packets = packetss[2]
# Function to generate sequential IP addresses in the 172.16.0.x range
def sequential_ip(start, end):
    for j in range(0, 10):
        for i in range(start, end + 1):
            yield f"192.{j}.0.{i}"

# Function to modify and send a packet
def modify_and_send_packet(pkt, src_ip, dst_ip, src_mac, dst_mac):
    # Modify IP layer
    if IP in pkt:
        pkt[IP].src = src_ip
        pkt[IP].dst = dst_ip
    
    # Modify Ethernet layer (MAC addresses)
    if Ether in pkt:
        pkt[Ether].src = src_mac
        pkt[Ether].dst = dst_mac
    
    # Recalculate checksums
    del pkt[IP].chksum
    del pkt[TCP].chksum
    
    # Send the packet
    # sendp(pkt, verbose=0)
    wrpcap("dnp3_attack_dos.pcap", pkt, append=True)

# Sequential IP range for DoS attack
start_ip = 1  # Start at 172.16.0.1
end_ip = 254  # End at 172.16.0.254

# MAC addresses to use
src_mac = 'be:0a:53:9f:cb:1b'
dst_mac = 'be:0a:50:6c:87:fa'

# Target IP for the attack
target_ip = "192.168.1.10"

# Loop through sequential IPs and modify the packet
for src_ip in sequential_ip(start_ip, end_ip):
    for pkt in packets:
        # Modify and send the packet
        modify_and_send_packet(pkt, src_ip, target_ip, src_mac, dst_mac)
        # Optional: Add delay to avoid immediate detection
        # time.sleep(0.1)
