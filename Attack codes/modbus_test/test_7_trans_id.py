from scapy.all import *

from scapy.all import *
from scapy.layers.inet import IP, TCP


input_file = "modbus200_github.pcapng"
output_file = "trans_github1.pcapng"


packets = rdpcap(input_file)


t=1

# Iterate through each packet
for packet in packets:
    if packet.haslayer(TCP):
        # Extract the TCP payload
        payload = bytes(packet[TCP].payload)
        # func_code = payload[7] if len(payload) > 7 else None
        # trans_id = int.from_bytes(payload[0:2], byteorder='big')
        # protocol_id = int.from_bytes(payload[2:4], byteorder='big')
        # unit_id = payload[6] if len(payload) > 6 else None
        
        # print(f"Transaction id : {trans_id}" )
        # print(f"Protocol id : {protocol_id}")
        # print(f"Unit id : {unit_id}")
        # print(f"Function code : {func_code}")
        
        
        
        
        if t == 198 or t == 199 :
            # Modify the transaction ID (first 2 bytes of payload)
            new_transaction_id = b'\x00\xB9'  #  new transaction ID
            modified_payload = new_transaction_id + payload[2:]
            
            # Modify the last byte of the payload
            # length = len(modified_payload)
            # new_value = b'\xc8'  # The new value to insert
            # modified_payload = modified_payload[:(length-1)] + new_value

            # Replace the original payload with the modified one
            packet[TCP].payload = Raw(modified_payload)
            
        

            # Recalculate checksums and lengths
            del packet[TCP].chksum  # Remove the old TCP checksum
            del packet[IP].len      # Remove the old IP length
            del packet[IP].chksum   # Remove the old IP checksum

            # Rebuild the packet to update checksums and lengths
            packet = packet.__class__(bytes(packet))

            # Save the modified packet to a new pcap file
            
            wrpcap(output_file, packet, append=True)
            
            
        t+=1

print("Done")	