from scapy.all import rdpcap, wrpcap
from scapy.layers.inet import TCP
from scapy.utils import hexdump

# Function to extract and modify the DNP3 application layer
def extract_dnp3_application_layer(pcap_file):
    # Read packets from the pcap file
    packets = rdpcap(pcap_file)
    
    # Only process the first two packets for this example
    packets_to_process = packets[20:22]
    
    for packet in packets_to_process:
        # Check if the packet has a TCP layer (DNP3 is usually over TCP/IP)
        if packet.haslayer(TCP):
            tcp_payload = bytes(packet[TCP].payload)
            
            # Assuming DNP3 application layer starts after TCP headers
            if len(tcp_payload) > 0:
                # Print the raw DNP3 application layer bytes
                print(f"Original Packet: {packet.summary()}")
                hexdump(tcp_payload)
                print("\n")
                
                # Example: Modify a specific byte in the application layer
                modified_payload = tcp_payload[:-7] + b'\x02' + tcp_payload[-6:]
                
                # Replace the original payload with the modified payload
                packet[TCP].remove_payload()
                packet[TCP].add_payload(modified_payload)
                
                # Recalculate the TCP checksum
                del packet[TCP].chksum
                
                # Append the modified packet to a new pcap file
                wrpcap('modified1.pcap', packet, append=True)
                
                print(f"Modified Packet: {packet.summary()}")
                hexdump(bytes(packet[TCP].payload))
                print("\n")
            else:
                print(f"Packet {packet.summary()} has no TCP payload.\n")

if __name__ == "__main__":
    pcap_file = "Supervised_200.pcap"
    extract_dnp3_application_layer(pcap_file)
