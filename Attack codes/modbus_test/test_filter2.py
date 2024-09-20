import pyshark
from scapy.all import wrpcap, Raw, IP, TCP

# Load the pcap file using PyShark and apply Modbus filter
file = "modbus200_github.pcapng"
cap = pyshark.FileCapture(file, display_filter='modbus')
# List to hold filtered Modbus packets for saving
modbus_packets = []

# Debug: Check if Modbus packets are being captured by PyShark
packet_count = 0

# Iterate through filtered packets and convert them to Scapy format
for packet in cap:
    packet_count += 1
    # print(f"Packet {packet_count}: {packet}")  # Print packet summary

    try:
        # Debug: Check if the Modbus layer exists
        if 'MODBUS' not in packet:
            print(f"Packet {packet_count} does not have Modbus layer.")
            continue

        ip_layer = IP(src=packet.ip.src, dst=packet.ip.dst)
        tcp_layer = TCP(sport=int(packet.tcp.srcport), dport=int(packet.tcp.dstport), seq=int(packet.tcp.seq))
        
        # Debug: Check Modbus field values (sometimes it might be different based on capture)
        print(f"Modbus field: {packet.modbus}")

        raw_data = Raw(load=bytes.fromhex(packet.modbus.field_value.replace(':', '')))
        scapy_pkt = ip_layer/tcp_layer/raw_data
        modbus_packets.append(scapy_pkt)

    except AttributeError as e:
        # Skip packets that don't have the required fields and print the error
        print(f"Error processing packet {packet_count}: {e}")
        continue

# Save the filtered Modbus packets to a new PCAP file
if modbus_packets:
    wrpcap('filtered_modbus.pcap', modbus_packets)
    print(f"Filtered {len(modbus_packets)} Modbus packets and saved to 'filtered_modbus.pcap'")
else:
    print("No Modbus packets were filtered.")

















# import pyshark
# from scapy.all import wrpcap, Raw, IP, TCP

# # Load the pcap file using PyShark and apply Modbus filter
# file = "modbus200_github.pcapng"
# cap = pyshark.FileCapture(file, display_filter='modbus')

# # List to hold filtered Modbus packets for saving
# modbus_packets = []

# # Iterate through filtered packets and convert them to Scapy format
# for packet in cap:
#     # Rebuild the packet in Scapy format (IP/TCP layers + Raw payload)
#     try:
#         ip_layer = IP(src=packet.ip.src, dst=packet.ip.dst)
#         tcp_layer = TCP(sport=int(packet.tcp.srcport), dport=int(packet.tcp.dstport), seq=int(packet.tcp.seq))
#         raw_data = Raw(load=bytes.fromhex(packet.modbus.field_value.replace(':', '')))
#         scapy_pkt = ip_layer/tcp_layer/raw_data
#         modbus_packets.append(scapy_pkt)
#     except AttributeError:
#         # Skip packets that don't have the required fields
#         continue

# # Save the filtered Modbus packets to a new PCAP file
# wrpcap('filtered_modbus1.pcap', modbus_packets)

# print(f"Filtered {len(modbus_packets)} Modbus packets and saved to 'filtered_modbus.pcap'")
