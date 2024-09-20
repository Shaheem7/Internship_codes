import pyshark
from scapy.all import wrpcap

# Step 1: Capture packets with both include_raw and use_json set to True
capture = pyshark.FileCapture('2024_02_20_CII_Lab_Modbus.pcapng', 
                              display_filter='modbus', 
                              include_raw=True, 
                              use_json=True)
                                
# Step 2: Collect raw Modbus packets
scapy_packets = []
for packet in capture:
    raw_packet = bytes(packet.get_raw_packet())  # Get raw packet bytes
    scapy_packets.append(raw_packet)
    
    # printing IP src and dst
    print(f"IP src: {packet['IP'].src} and IP dst: {packet['IP'].dst}")
    # scapy_packets.append(packet)

# Step 3: Write the filtered Modbus packets to a new PCAP file
wrpcap('filtered_new_modbus3.pcap', scapy_packets)
print("[+] Modbus packets written to filtered_new_modbus3.pcap")