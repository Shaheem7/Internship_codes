from scapy.all import rdpcap, wrpcap, Raw

# Configuration
input_pcap = 'dnp3_example.pcap' 
output_pcap = 'output_modified_s44.pcap'
byte_index = -4
new_value = 0xFF 

# Read packets from the input pcap file
packets = rdpcap(input_pcap)
modified_packets = []

pkts = packets[2:3]
# Process each packet
for packet in packets:
    packet_bytes = bytes(packet)  # Convert the packet to bytes
    packet.show()
    print(packet_bytes)
    print(len(packet_bytes))
    if byte_index < len(packet_bytes):
        # Modify the specific byte
        modified_bytes = bytearray(packet_bytes)
        print(modified_bytes)
        modified_bytes[byte_index] = new_value
        
        # Create a new Raw packet with the modified bytes
        modified_packet = Raw(load=bytes(modified_bytes))
        modified_packets.append(modified_packet)

# Write the modified packets to a new pcap file
wrpcap(output_pcap, modified_packets)

print(f"Modified pcap file saved as {output_pcap}")
