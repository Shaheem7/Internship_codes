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
                    # Modify the function code in the payload
                    modified_payload = (
                        payload[:function_code_pos] +
                        bytes([new_function_code]) +
                        payload[function_code_pos + 1:]
                    )
                    
                    # Rebuild the TCP packet with the modified payload
                    new_tcp_segment = TCP(
                        sport=packet[TCP].sport,
                        dport=packet[TCP].dport,
                        seq=packet[TCP].seq,
                        ack=packet[TCP].ack,
                        dataofs=packet[TCP].dataofs,
                        flags=packet[TCP].flags,
                        window=packet[TCP].window,
                        chksum=0,  # Will be recalculated
                        urgptr=packet[TCP].urgptr,
                        options=packet[TCP].options
                    )
                    
                    # Rebuild the IP packet with the new TCP segment
                    new_ip_packet = IP(
                        src=packet[IP].src,
                        dst=packet[IP].dst,
                        ihl=packet[IP].ihl,
                        version=packet[IP].version,
                        tos=packet[IP].tos,
                        len=0,  # Will be recalculated
                        id=packet[IP].id,
                        flags=packet[IP].flags,
                        frag=packet[IP].frag,
                        ttl=packet[IP].ttl,
                        proto=packet[IP].proto,
                        chksum=0,  # Will be recalculated
                        options=packet[IP].options
                    ) / new_tcp_segment / Raw(load=modified_payload)

                    # Return the new packet
                    return new_ip_packet

    # Return the original packet if no modifications were made
    return packet

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
