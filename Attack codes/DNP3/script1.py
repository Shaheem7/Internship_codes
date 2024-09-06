from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

def modify_dnp3_function_code(packet, new_function_code):
    """ Modify the DNP3 function code in the packet if it's a valid DNP3 packet. """
    if TCP in packet and packet[TCP].dport == 20000:  # Check if it's a TCP packet on port 20000 (DNP3)
        payload = bytes(packet[TCP].payload)
        
        if len(payload) > 6:  # Basic length check to ensure there's enough data
            # Check if the payload contains DNP3 data
            dnp3_start = payload.find(b'\x05\x64')  # DNP3 data link layer start bytes
            if dnp3_start != -1:
                # Find the function code position (typically after DNP3 header)
                function_code_pos = dnp3_start + 11  # Adjust as needed based on DNP3 structure
                if function_code_pos < len(payload):
                    modified_payload = (
                        payload[:function_code_pos] +
                        bytes([new_function_code]) +
                        payload[function_code_pos + 1:]
                    )
                    return packet[:TCP].payload(modified_payload)  # Create a new packet with modified payload
    return packet  # Return original packet if no modifications were made

def process_pcap(input_file, output_file, new_function_code):
    """ Process the pcap file to modify DNP3 function codes and save to a new file. """
    packets = rdpcap(input_file)  # Read packets from the input pcap file
    modified_packets = []

    for packet in packets:
        modified_packet = modify_dnp3_function_code(packet, new_function_code)
        modified_packets.append(modified_packet)

    wrpcap(output_file, modified_packets)  # Write modified packets to the output pcap file

if __name__ == "__main__":
    input_pcap = 'Supervised_200.pcap'  # Path to the input pcap file
    output_pcap = 'output_modified.pcap'  # Path to the output pcap file
    new_function_code = 0x02  # New function code to be set

    process_pcap(input_pcap, output_pcap, new_function_code)
    print(f"Modified pcap file saved as {output_pcap}")
