from scapy.all import *

file = "Modbus_VJTI_2k.pcapng"


pkts = rdpcap(file)

pkt = pkts[0:100] + pkts[40:50] + pkts[100:150]


wrpcap("modbus_replay.pcapng", pkt, append=True)
    