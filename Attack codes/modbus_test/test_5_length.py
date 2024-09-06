from scapy.all import *
from scapy.layers.inet import IP, TCP

input_file = "modbus200_github.pcapng"
output_file = "change_in_length.pcapng"

packets = rdpcap(input_file)

for packet in packets:
    assert packet.haslayer(TCP)
    
    if packet.haslayer(TCP):
        payload = bytes(packet[TCP].payload)
        length = len(payload)
        
        print(length)
        print(payload)
        print(payload[5])
        
        new_value = length + 5
        
        # Convert new_value to a byte
        new_value_byte = bytes([new_value])
        
        modified_payload = payload[:5] + new_value_byte + payload[6:]
        print(modified_payload)
        
        packet[TCP].payload = Raw(modified_payload)
        
        # Recalculate the checksums and lengths
        del packet[TCP].chksum  # Remove old checksum
        del packet[IP].len      # Remove old length
        del packet[IP].chksum   # Remove old IP checksum
    
        # Recalculate checksums and lengths
        packet = packet.__class__(bytes(packet))
    
        # Save the modified packet to a new pcap file
        wrpcap(output_file, packet, append=True)








# from scapy.all import *
# from scapy.layers.inet import IP, TCP


# input_file = "modbus200_github.pcapng"


# output_file = "change_in_length.pcapng"
# packets = rdpcap(input_file)




# for packet in packets:
    
#     assert packet.haslayer(TCP)
    
#     if packet.haslayer(TCP):
        
#         payload = bytes(packet[TCP].payload)
#         length = len(payload)
        
#         print(length)
#         print(payload)
#         print(payload[5])
        
#         # new_value = b'\x90'  
#         new_value = length + 5
#         new_length = b'\x00' + bytes([new_value])
        
#         modified_payload = payload[:5] + new_value + payload[7:]
#         print(modified_payload)
        
#         packet[TCP].payload = Raw(modified_payload)
        
    
#     # Recalculate the checksums and lengths
#     del packet[TCP].chksum  # Remove old checksum
#     del packet[IP].len      # Remove old length
#     del packet[IP].chksum   # Remove old IP checksum
    
#     # Recalculate checksums and lengths
    
#     packet = packet.__class__(bytes(packet))
    
    

#     # Save the modified packet to a new pcap file
   
#     wrpcap(output_file, packet, append=True)