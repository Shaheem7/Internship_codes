from scapy.all import *
from pymodbus.constants import Endian, RegisterType
from pymodbus.pdu import ModbusRequest, ModbusResponse
from scapy.layers.inet import IP, TCP

# Define the path to your PCAP file and the output PCAP file
input_pcap_file = '2024_02_20_CII_Lab_Modbus.pcapng'
output_pcap_file = 'modified_modbus_traffic.pcap'

# Function to parse and manipulate Modbus TCP packets
def manipulate_modbus_packet(packet):
    # Check if the packet contains a TCP layer
    if packet.haslayer(TCP):
        # Extract the TCP payload
        tcp_payload = bytes(packet[TCP].payload)
        
        # Ensure the TCP payload is long enough to contain a Modbus TCP header
        if len(tcp_payload) >= 12:  # Minimum length of Modbus TCP header
            # Extract Modbus TCP header fields
            transaction_id = int.from_bytes(tcp_payload[0:2], byteorder='big')
            protocol_id = int.from_bytes(tcp_payload[2:4], byteorder='big')
            length = int.from_bytes(tcp_payload[4:6], byteorder='big')
            unit_id = tcp_payload[6]
            function_code = tcp_payload[7]

            # Check if the protocol ID is 0 (Modbus TCP)
            if protocol_id == 0:
                # Print extracted Modbus TCP header fields for debugging
                print(f"Transaction ID: {transaction_id}, Protocol ID: {protocol_id}, Length: {length}, Unit ID: {unit_id}, Function Code: {function_code}")

                # Only process Modbus packets with specific function codes
                if function_code == 0x10:  # Write Multiple Registers
                    starting_address = int.from_bytes(tcp_payload[8:10], byteorder='big')
                    quantity = int.from_bytes(tcp_payload[10:12], byteorder='big')
                    byte_count = tcp_payload[12]
                    values = tcp_payload[13:13 + byte_count]

                    # Create a new payload for Write Single Register
                    new_function_code = 0x06  # Write Single Register
                    if len(values) >= 2:
                        register_value = int.from_bytes(values[:2], byteorder='big')

                        # New payload for Write Single Register
                        modified_payload = (
                            tcp_payload[:7] +  # Copy header up to unit_id
                            bytes([new_function_code]) +  # New function code
                            starting_address.to_bytes(2, byteorder='big') +  # Address
                            register_value.to_bytes(2, byteorder='big')  # Register value
                        )

                        # Replace the payload with the modified payload
                        packet[TCP].payload = Raw(load=modified_payload)
                        
                        # Recalculate TCP checksum
                        del packet[TCP].chksum
                        packet = packet.__class__(bytes(packet))

    return packet

# Load the PCAP file
packets = rdpcap(input_pcap_file)

# List to store manipulated packets
modified_packets = []

# Iterate through each packet in the PCAP file
for packet in packets:
    # Manipulate the packet if it's a Modbus packet
    modified_packet = manipulate_modbus_packet(packet)
    modified_packets.append(modified_packet)

# Save the modified packets to a new PCAP file
wrpcap(output_pcap_file, modified_packets)

print(f"Modified packets saved to {output_pcap_file}")
