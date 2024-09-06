from scapy.all import *



file1 = 'Supervised.pcap'

packets = rdpcap(file1)

pkts = packets[:200]

wrpcap('Supervised_200.pcap', pkts)
print('Done')