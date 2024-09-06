from scapy.all import *
from scapy.layers.inet import IP, TCP



input_pcap_file = "modbusBig_github.pcap"  
output_pcap_file = "change_func_code_2.pcapng"  

# Read packets from the input pcap file
packets = rdpcap(input_pcap_file)

# Iterate over packets and modify function codes
for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        if len(payload) > 7:                        # Ensure there is enough data for Modbus
            function_code = payload[7]
            if function_code == 0x01:               # Check if function code is 0x0x
                
                modified_payload = (payload[:7] + bytes([0x02]) + payload[8:])     # Update function code to 0x0y
                packet[Raw].load = modified_payload
                del packet[TCP].chksum  # Remove TCP checksum to force recalculation
                del packet[IP].chksum   # Remove IP checksum to force recalculation
                
                
                
            elif function_code == 0x05:               # Check if function code is 0x0x
                
                modified_payload = (payload[:7] + bytes([0x06]) + payload[8:])     # Update function code to 0x0y
                packet[Raw].load = modified_payload
                del packet[TCP].chksum  # Remove TCP checksum to force recalculation
                del packet[IP].chksum   # Remove IP checksum to force recalculation
                
                

# Write the modified packets to a new pcap file
wrpcap(output_pcap_file, packets)

print("Done")
