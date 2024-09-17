from scapy.all import *
from scapy.layers.inet import IP, TCP

input_pcap_file = "modbus200_github.pcapng"  
output_pcap_file = "change_rv_func_ref.pcapng"  

packets = rdpcap(input_pcap_file)

# Internet Protocol Version 4, Src: 10.235.149.240, Dst: 10.235.149.243

source_ip = "10.235.149.240"
modified_packets = []

for packet in packets:
    if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
        raw_bytes = bytearray(packet[Raw].load)  # Use bytearray for mutability
        
        
        payload = packet[Raw].load
        function_code = payload[7]
        
        
        # make sure the packet is from the source IP  so that it will be a { request packet }
        if packet[IP].src == source_ip:
            # Modify the reference number (last 4 bytes)
            raw_bytes[-4:-2] = b'\x00\x09'
            
            # Modify the function code
            if function_code == 0x01:
                raw_bytes[7] = 0x02
            elif function_code == 0x05:                
                raw_bytes[7] = 0x06
        
        else:
            # Modify the function code
            if function_code == 0x01:
                raw_bytes[7] = 0x02
            elif function_code == 0x05:                
                raw_bytes[7] = 0x06
            
            # Modify the register value (last 2 bytes)
            raw_bytes[-2:] = b'\x00\x01'
        
        # Update the Raw payload with modified bytes
        packet[Raw].load = bytes(raw_bytes)
        
        # Recalculate checksums
        del packet[TCP].chksum
        del packet[IP].chksum
        
        # Append the modified packet to the new list
        modified_packets.append(packet)
    else:
        # If the packet doesn't need modification, append it as is
        modified_packets.append(packet)

# Write the modified packets to a new pcap file
wrpcap(output_pcap_file, modified_packets)

print("Done")




