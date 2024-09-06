from scapy.all import rdpcap, wrpcap, Ether, IP, TCP, Raw
from scapy.utils import checksum

# Configuration
input_pcap = 'dnp3_example.pcap'
output_pcap = 'output_modified_s31.pcap'
byte_index = -4
new_value = 0xFF

# Read packets from the input pcap file
packets = rdpcap(input_pcap)
modified_packets = []

# Define header lengths in bytes
ETHERNET_HEADER_LEN = 14
IP_HEADER_LEN = 20
TCP_HEADER_LEN = 20

# Function to calculate checksum
def compute_checksum(data):
    return checksum(data)

# Process each packet
for packet in packets:
    if Raw in packet:
        # Convert packet to bytearray and modify the specified byte
        packet_bytes = bytes(packet)
        modified_bytes = bytearray(packet_bytes)
        if byte_index < len(modified_bytes):
            modified_bytes[byte_index] = new_value

        # Extract layers from modified bytes
        ether_layer = Ether(modified_bytes[:ETHERNET_HEADER_LEN])
        ip_layer = IP(modified_bytes[ETHERNET_HEADER_LEN:ETHERNET_HEADER_LEN + IP_HEADER_LEN])
        tcp_layer = TCP(modified_bytes[ETHERNET_HEADER_LEN + IP_HEADER_LEN:ETHERNET_HEADER_LEN + IP_HEADER_LEN + TCP_HEADER_LEN])
        raw_data = modified_bytes[ETHERNET_HEADER_LEN + IP_HEADER_LEN + TCP_HEADER_LEN:]

        # Rebuild the packet
        new_packet = ether_layer / ip_layer / tcp_layer / Raw(load=raw_data)

        # Calculate and update checksums
        ip_header_bytes = bytes(new_packet[IP])
        tcp_header_bytes = bytes(new_packet[TCP])
        raw_data_bytes = bytes(new_packet[Raw])

        # Recalculate IP checksum
        new_packet[IP].chksum = compute_checksum(ip_header_bytes)

        # Recalculate TCP checksum
        pseudo_header = (
            ip_header_bytes[12:16] +  # Source IP
            ip_header_bytes[16:20] +  # Destination IP
            b'\x00' * 1 +  # Placeholder for protocol
            b'\x06' +  # TCP Protocol
            len(tcp_header_bytes + raw_data_bytes).to_bytes(2, 'big')
        )
        tcp_checksum = compute_checksum(pseudo_header + tcp_header_bytes + raw_data_bytes)
        new_packet[TCP].chksum = tcp_checksum

        # Add the modified packet to the list
        modified_packets.append(new_packet)

# Write the modified packets to a new pcap file
wrpcap(output_pcap, modified_packets)

print(f"Modified pcap file saved as {output_pcap}")
