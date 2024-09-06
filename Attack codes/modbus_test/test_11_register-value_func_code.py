from scapy.all import *
from scapy.layers.inet import IP, TCP

input_pcap_file = "modbus200_github.pcapng"
output_pcap_file = "change_func_code_rv.pcapng"  

# Read packets from the input pcap file
packets = rdpcap(input_pcap_file)

# Iterate over packets and modify function codes and last two bytes
for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        if len(payload) > 7:  # Ensure there is enough data for Modbus
            function_code = payload[7]
            if function_code == 0x01:  
                
                # Modify the function code
                modified_payload = (payload[:7] + bytes([0x02]) + payload[8:])
                
            elif function_code == 0x05:  
                
                # Modify the function code
                modified_payload = (payload[:7] + bytes([0x06]) + payload[8:])
                
                
            modified_payload = modified_payload[:-2] + b'\x00\x01'
                
            packet[Raw].load = modified_payload
            del packet[TCP].chksum  # Remove TCP checksum to force recalculation
            del packet[IP].chksum   # Remove IP checksum to force recalculation

# Write the modified packets to a new pcap file
wrpcap(output_pcap_file, packets)

print("Done")
