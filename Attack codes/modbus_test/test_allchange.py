from scapy.all import *
from scapy.layers.inet import IP, TCP

input_pcap_file = "modbus200_github.pcapng"  
output_pcap_file = "change_rv_func_ref.pcapng"  

packets = rdpcap(input_pcap_file)

# Internet Protocol Version 4, Src: 10.235.149.240, Dst: 10.235.149.243

source_ip = "10.235.149.240"
modified_packets = []

for packet in packets:
    if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
        raw_bytes = bytearray(packet[Raw].load)  # Use bytearray for mutability
        
        
        payload = packet[Raw].load
        function_code = payload[7]
        
        if packet[IP].src == source_ip:
            # Modify the reference number (last 4 bytes)
            raw_bytes[-4:-2] = b'\x00\x09'
            
            # Modify the function code
            if function_code == 0x01:
                raw_bytes[7] = 0x02
            elif function_code == 0x05:                
                raw_bytes[7] = 0x06
        
        else:
            # Modify the function code
            if function_code == 0x01:
                raw_bytes[7] = 0x02
            elif function_code == 0x05:                
                raw_bytes[7] = 0x06
            
            # Modify the register value (last 2 bytes)
            raw_bytes[-2:] = b'\x00\x01'
        
        # Update the Raw payload with modified bytes
        packet[Raw].load = bytes(raw_bytes)
        
        # Recalculate checksums
        del packet[TCP].chksum
        del packet[IP].chksum
        
        # Append the modified packet to the new list
        modified_packets.append(packet)
    else:
        # If the packet doesn't need modification, append it as is
        modified_packets.append(packet)

# Write the modified packets to a new pcap file
wrpcap(output_pcap_file, modified_packets)

print("Done")









# from scapy.all import *
# from scapy.layers.inet import IP, TCP

# input_pcap_file = "Modbus_VJTI_2k.pcapng"  
# output_pcap_file = "rv_func_len1.pcapng"  

# packets = rdpcap(input_pcap_file)

# source_ip = "172.16.0.79"

# modified_packets = []

# for packet in packets:
#     if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
#         raw_bytes = bytes(packet[Raw].load)
        
#         if packet[IP].src == source_ip:
#             # Change the reference number (last 4 bytes)
#             modified_bytes = raw_bytes[:-4] + b'\x00\x09' + raw_bytes[-2:]
        
#         else:
#             # Change the function code (assuming it's at position 61)
#             modified_bytes = raw_bytes[:61] + bytes([0x02]) + raw_bytes[62:]
            
#             # Change the register value (last 2 bytes)
#             modified_bytes = modified_bytes[:-2] + b'\x00\x01'
        
#         # Replace the Raw layer's load with modified bytes
#         packet[Raw].load = modified_bytes
        
#         # Recalculate checksums
#         del packet[TCP].chksum
#         del packet[IP].chksum
        
#         # Append modified packet to the list
#         modified_packets.append(packet)
#     else:
#         # If no modifications are needed, append the original packet
#         modified_packets.append(packet)

# # Write the modified packets to a new pcap file
# wrpcap(output_pcap_file, modified_packets)

# print("Done")











# from scapy.all import *
# from scapy.layers.inet import IP, TCP

# input_pcap_file = "Modbus_VJTI_2k.pcapng"  
# output_pcap_file = "rv_func_len.pcapng"  


# packets = rdpcap(input_pcap_file)


# # Internet Protocol Version 4, Src: 172.16.0.79, Dst: 172.16.0.20

# source_ip = "172.16.0.79"  

# for packet in packets:
#     if packet.haslayer(IP):

#         raw_bytes = bytes(packet)
#         if packet[IP].src == source_ip:
            
#             # change the reference number
#             modified_bytes = raw_bytes[:-4] + b'\x00\x09' + raw_bytes[-2:]
        
#         # Reconstruct the packet from the modified bytes
#             modified_packet = Raw(load=modified_bytes)
            
#             # Update the packet in the list
#             packet = modified_packet    
       
        
#         else:
            
#             # function code
#             modified_bytes = raw_bytes[:61] + bytes([0x02]) + raw_bytes[62:]
                
#             # change the register value
#             modified_bytes = modified_bytes[:-2] + b'\x00\x01'
            
#              # Reconstruct the packet from the modified bytes
#             modified_packet = Raw(load=modified_bytes)
            
                
#             # Update the packet in the list
#             packet = modified_packet    

#             # del packet[TCP].chksum  # Remove TCP checksum to force recalculation
#             # del packet[IP].chksum   # Remove IP checksum to force recalculation

# # Write the modified packets to a new pcap file
# wrpcap(output_pcap_file, packets)

# print("Done")
