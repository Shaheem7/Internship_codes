from scapy.all import rdpcap, wrpcap, TCP
from scapy.layers.inet import IP, Ether 

# import raw
from scapy.layers.l2 import Ether  


# Load the pcap file

file = "2024_02_20_CII_Lab_Modbus.pcapng"
packets = rdpcap(file)

print(packets[0])

print(packets[0].show())    

print("\n\n")

print(packets[0].summary())

print("\n\n")

print(packets[0].command())

print("\n\n")

print("Time of the first packet: ")
print(packets[0].time)

print("\n\n")

print(packets[0].load)

packet = packets[0]




# Filter Modbus TCP packets (TCP on port 502)
modbus_packets = [pkt for pkt in packets if TCP in pkt and (pkt[TCP].dport == 502 or pkt[TCP].sport == 502)]

# Write the filtered Modbus packets to a new PCAP file
wrpcap('filtered_modbus.pcap', modbus_packets)

print(f"Filtered {len(modbus_packets)} Modbus packets and saved to 'filtered_modbus.pcap'")
