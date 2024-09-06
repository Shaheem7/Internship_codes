from scapy.all import *

# Capture a Modbus TCP packet
# pkt = sniff(filter="tcp port 502", count=1)[0]

file = "modbus_12.pcapng"
packets = rdpcap(file)

pkt = packets[0]

# Extract the Modbus TCP header (first 6 bytes)
modbus_header = pkt[Raw].load[:6]

# Extract the length field (bytes 5 and 6)
length_bytes = modbus_header[4:6]

# Convert the length field to an integer
original_length = int.from_bytes(length_bytes, byteorder='big')
print(f"Original Length: {original_length}")

# Modify the length field (example: increase by 2)
new_length = original_length + 2
new_length_bytes = new_length.to_bytes(2, byteorder='big')

# Replace the length field in the header
new_modbus_header = modbus_header[:4] + new_length_bytes + modbus_header[6:]
print(f"New Modbus Header: {new_modbus_header}")
print(f"New Length: {new_length}")

# Update the packet with the modified header
pkt[Raw].load = new_modbus_header + pkt[Raw].load[6:]

# Send the modified packet
wrpcap("modified_modbus_packet.pcap", pkt ,append = True        )
