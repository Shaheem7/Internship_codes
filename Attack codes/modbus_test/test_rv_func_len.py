from scapy.all import *
from scapy.layers.inet import IP, TCP

input_pcap_file = "modbus200_github.pcapng"  
output_pcap_file = "change_rv_func_len.pcapng"  

# Read packets from the input pcap file
packets = rdpcap(input_pcap_file)

# Iterate over packets and modify function codes, last two bytes, and length
for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        if len(payload) > 7:  # Ensure there is enough data for Modbus
            function_code = payload[7]
            if function_code == 0x01:
                
                # Update function code to 0x0f
                modified_payload = (payload[:7] + bytes([0x02]) + payload[8:])
                
                # Modify the last two bytes for changing the register value
                if len(modified_payload) > 2:
                    modified_payload = modified_payload[:-2] + b'\x00\x01'
                
                # Modify the length field (bytes 4 and 5)
                new_length = (len(modified_payload) - 6 ) + 10 # Exclude the first 6 bytes of the header
                # new_length = 2000
                length_bytes = new_length.to_bytes(2, byteorder='big')
                modified_payload = modified_payload[:4] + length_bytes + modified_payload[6:]
                
                packet[Raw].load = modified_payload
                del packet[TCP].chksum  # Remove TCP checksum to force recalculation
                del packet[IP].chksum   # Remove IP checksum to force recalculation
  
  
            elif function_code == 0x05:
                
                # Update function code to 0x0f
                modified_payload = (payload[:7] + bytes([0x06]) + payload[8:])
                
                # Modify the last two bytes for changing the register value
                if len(modified_payload) > 2:
                    modified_payload = modified_payload[:-2] + b'\x00\x01'
                
                # Modify the length field (bytes 4 and 5)
                new_length = (len(modified_payload) - 6 ) + 10 
                # new_length = 2000
                length_bytes = new_length.to_bytes(2, byteorder='big')
                modified_payload = modified_payload[:4] + length_bytes + modified_payload[6:]
                
                packet[Raw].load = modified_payload
                del packet[TCP].chksum  # Remove TCP checksum to force recalculation
                del packet[IP].chksum   # Remove IP checksum to force recalculation



# Write the modified packets to a new pcap file
wrpcap(output_pcap_file, packets)

print("Done")
