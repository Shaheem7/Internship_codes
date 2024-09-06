from scapy.all import *

file = "Modbus_VJTI_2k.pcapng"

packets = rdpcap(file)

pkts = packets[1:11]

wrpcap("modbus_attack_replay_10pkts.pcap", pkts, append=True)