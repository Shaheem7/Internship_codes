from scapy.all import *
from pymodbus.pdu import ModbusRequest, ModbusResponse
from pymodbus.client import ModbusTcpClient

from scapy.layers.inet import IP, TCP

# Define the path to your PCAP file and the output PCAP file
input_pcap_file = '2024_02_20_CII_Lab_Modbus.pcapng'
output_pcap_file = 'modified_modbus_traffic.pcap'

# Function to parse and manipulate Modbus TCP packets
def manipulate_modbus_packet(packet):
    
    # Check if the packet contains Modbus TCP traffic
    if packet.haslayer(TCP):
        payload = bytes(packet[TCP].payload)
        
        # Extract Modbus function code (example: read holding registers)
        if len(payload) > 6:                 # Modbus application data unit length check
            
            transaction_id = int.from_bytes(payload[0:2], byteorder='big')
            protocol_id = int.from_bytes(payload[2:4], byteorder='big')
            length = int.from_bytes(payload[4:6], byteorder='big')
            unit_id = payload[6]
            function_code = payload[7]

            print(f'''Transaction ID: {transaction_id},
                  Protocol ID: {protocol_id},
                    Length: {length},
                    Unit ID: {unit_id}, 
                  Function Code: {function_code}''')

            # Example of modifying the function code (e.g., changing a read to a write)
            if function_code == 0x03:  # If it's a "Read Holding Registers" function
                new_function_code = 0x06  # Change to "Write Multiple Registers"
                modified_payload = payload[:7] + bytes([new_function_code]) + payload[8:]
                
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

print(f"Total packets processed: {len(modified_packets)}")
print(f"Modified packets saved to {output_pcap_file}")
