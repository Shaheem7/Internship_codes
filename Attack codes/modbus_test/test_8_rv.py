from scapy.all import *
from scapy.layers.inet import IP, TCP

input_pcap_file = "modbusBig_github.pcap"  
output_pcap_file = "change_rv2.pcapng"  

# Read packets from the input pcap file
packets = rdpcap(input_pcap_file)



source_ip = "10.235.149.243"  

for packet in packets:
    if packet.haslayer(IP) and packet[IP].src == source_ip:
        # Get the raw bytes of the packet
        raw_bytes = bytes(packet)
        
        modified_bytes = raw_bytes[:-2] + b'\x00\x01'
        
        
        # Reconstruct the packet from the modified bytes
        modified_packet = Raw(load=modified_bytes)
        
        # Update the packet in the list
        packet = modified_packet

# Save the modified packets to a new pcap file
    wrpcap(output_pcap_file, packet,append=True)

print("Done")


# # Iterate over packets and modify function codes and last two bytes
# for packet in packets:
#     if packet.haslayer(TCP) and packet.haslayer(Raw):
#         payload = packet[Raw].load
#         if len(payload) > 7:  # Ensure there is enough data for Modbus
#             function_code = payload[7]
           

#             payload = payload[:-2] + b'\x00\x01'
            
#             packet[Raw].load = payload
#             del packet[TCP].chksum  # Remove TCP checksum to force recalculation
#             del packet[IP].chksum   # Remove IP checksum to force recalculation

# # Write the modified packets to a new pcap file
# wrpcap(output_pcap_file, packets)

# print("Done")
