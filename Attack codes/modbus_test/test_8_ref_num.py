from scapy.all import *
from scapy.layers.inet import IP, TCP

file_input = "modbusBig_github.pcap"  # Input pcap file
file_output = "change_ref_num.pcapng"   # Output pcap file

# Read packets from the input file
packets = rdpcap(file_input)

# Internet Protocol Version 4, Src: , Dst: 172.16.0.20
# Internet Protocol Version 4, Src: 10.235.149.240, Dst: 10.235.149.243

source_ip = "10.235.149.240"  

for packet in packets:
    if packet.haslayer(IP) and packet[IP].src == source_ip:
        # Get the raw bytes of the packet
        raw_bytes = bytes(packet)
        
        # Modify the last 3 to 5 bytes
        # Here we assume you want to replace the last 5 bytes
        modified_bytes = raw_bytes[:-4] + b'\x00\x09' + raw_bytes[-2:]
        
        # Reconstruct the packet from the modified bytes
        modified_packet = Raw(load=modified_bytes)
        
        # Update the packet in the list
        packet = modified_packet

# Save the modified packets to a new pcap file
    wrpcap(file_output, packet,append=True)

print("Done")
