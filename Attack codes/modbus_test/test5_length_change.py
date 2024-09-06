from scapy.all import *
from scapy.layers.inet import IP, TCP

input_file = "modbus200_github.pcapng"
output_file = "change_in_length1.pcapng"

packets = rdpcap(input_file)

for packet in packets:
    if packet.haslayer(TCP):
        # Get the payload
        payload = bytes(packet[TCP].payload)
        
        # Calculate new length (length of payload + 5)
        new_length = len(payload) + 5
        
        # Modify the payload (e.g., change the 6th byte to the new length)
        modified_payload = payload[:5] + bytes([new_length]) + payload[6:]
        
        # Assign the modified payload back to the packet
        packet[TCP].payload = Raw(modified_payload)
        
        # Let Scapy recalculate the checksums and lengths automatically
        del packet[IP].len      # Remove old length
        del packet[IP].chksum   # Remove old IP checksum
        del packet[TCP].chksum  # Remove old TCP checksum
        
        # Save the modified packet to the new pcap file
        wrpcap(output_file, packet, append=True)


print("Done")