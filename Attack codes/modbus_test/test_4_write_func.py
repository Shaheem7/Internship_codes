from scapy.all import *
from scapy.layers.inet import IP, TCP


file = "modbus_12.pcapng"

packets = rdpcap(file)


for packet in packets:
    
    if packet.haslayer(TCP):
        
        payload = bytes(packet[TCP].payload)
        
        leng = len(packet)

        func_code = payload[7]
        
        
        if func_code == 0x06 or leng == 65 :       # write single register
            
            length = len(packet[TCP].payload)
            new_value = b'\xc8' 
            modified_payload = payload[:(length-1)] + new_value

            packet[TCP].payload = Raw(modified_payload)


    # Recalculate the checksums and lengths
    del packet[TCP].chksum  # Remove old checksum
    del packet[IP].len      # Remove old length
    del packet[IP].chksum   # Remove old IP checksum

    # Recalculate checksums and lengths
    packet = packet.__class__(bytes(packet))
    
    

    # Save the modified packet to a new pcap file
    new_file = "test_4_v3.pcapng"
    wrpcap(new_file, packet, append=True)
    



