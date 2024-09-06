from scapy.all import *
from scapy.layers.inet import IP, TCP
from time import time



# file1 = "modbus200_github.pcapng"
file1 = "change_rv_func_ref.pcapng"
file2 = "trans_github1.pcapng"

packets1 = rdpcap(file1)
packets2 = rdpcap(file2)


packets3 = packets1[:197]


# packets3 = packets1[:6] + packets1[4:6] + packets1[6:]
# packets3 = packets1 + packets2 

pkts = packets3 + packets2
# pkts = packets1 + packets2

output_file = "allchange.pcapng"
wrpcap(output_file, pkts, append=True)


print("Done")