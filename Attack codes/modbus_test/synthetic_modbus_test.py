# Imports 
import os, sys, argparse
from scapy.all import *
from scapy.layers.inet import IP, TCP

# Use argparse to parse command line arguments
if len(sys.argv) < 2:
    print('[-] For help menu, use -h')
    sys.exit(1)

less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=8)

parser = argparse.ArgumentParser(description='Modbus Packet Modifier.', formatter_class=less_indent_formatter)
parser.add_argument('-i', '--input', required=True, help='Input pcap file')
parser.add_argument('-o', '--output', required=True, help='Output pcap file')
parser.add_argument('-s', '--src_ip', required=True, help='Source IP address to filter')

args = parser.parse_args()

# Read from pcap
input_pcap_file = args.input
output_pcap_file = args.output
source_ip = args.src_ip

packets = rdpcap(input_pcap_file)
modified_packets = []

# Iterate through packets and modify as needed
for packet in packets:
    if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
        raw_bytes = bytearray(packet[Raw].load)  # Use bytearray for mutability
        payload = packet[Raw].load
        function_code = payload[7]
        
        if packet[IP].src == source_ip:
            # Modify the reference number 
            raw_bytes[-4:-2] = b'\x00\x09'
            
            # Modify the function code based on conditions
            if function_code == 0x01:
                raw_bytes[7] = 0x02
            elif function_code == 0x05:
                raw_bytes[7] = 0x06
        
        # Replace the modified payload with new data
        packet[Raw].load = bytes(raw_bytes)
        
    modified_packets.append(packet)

# Write the modified packets to the output pcap file
wrpcap(output_pcap_file, modified_packets)

print(f'[+] Modified pcap saved to {output_pcap_file}')
