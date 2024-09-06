from scapy.all import *

from scapy.layers.inet import IP

# Load the Modbus pcap
packetss = rdpcap("Modbus_VJTI_2k.pcapng")

packets = packetss[0:30]

# Internet Protocol Version 4, Src: 172.16.0.20, Dst: 172.16.0.79

c = 0
# Modify source/destination IP or ports (if needed)
for pkt in packets:
    if c % 2 == 0:
        if IP in pkt:
            pkt[IP].src = "172.16.0.20"
            pkt[IP].dst = "172.16.0.30"
    else:
        if IP in pkt:
            pkt[IP].src = "172.16.0.30"
            pkt[IP].dst = "172.16.0.20"
    
    c += 1

# Save the modified pcap
# wrpcap("modbus_attack_replay.pcap", packets, append=True)
sendp(packets, verbose=False)
