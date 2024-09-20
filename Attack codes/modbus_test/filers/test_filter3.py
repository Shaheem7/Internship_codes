import pyshark
from scapy.all import rdpcap
# Load the PCAP file with PyShark
file = "2024_02_20_CII_Lab_Modbus.pcapng"
capture = pyshark.FileCapture('', display_filter='tcp.port == 502')



# for packet in capture:
#     print(packet)

packets = rdpcap(file)
print(packets[0])

print(f"Filtered {len(capture)} Modbus packets")





# from scapy.all import rdpcap

# # Load the PCAP file
# packets = rdpcap("modbus200_github.pcapng")

# # Filter Modbus TCP packets
# modbus_packets = [pkt for pkt in packets if pkt.haslayer('TCP') and pkt['Raw'].load.startswith(b'\x00\x00')]
# for pkt in modbus_packets:
#     print(pkt.summary())

# print(f"Filtered {len(modbus_packets)} Modbus packets")