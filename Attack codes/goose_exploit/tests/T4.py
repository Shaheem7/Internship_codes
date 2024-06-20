 ###############################
# Import Python modules
###############################
import os, sys, datetime, inspect, struct, time
from copy import deepcopy

###############################
# Import SCAPY and ASN1 modules
###############################
from pyasn1.codec.ber import decoder
from pyasn1.codec.ber import encoder
from pyasn1.type import char
from pyasn1.type import tag
from pyasn1.type import univ
from scapy.layers.l2 import Ether
from scapy.layers.l2 import Dot1Q
from scapy.compat import raw
from scapy.all import rdpcap
from scapy.utils import wrpcap

###############################
# Import Goose module
###############################
# We have to tell script where to find the Goose module in parent directory
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from goose.goose import GOOSE
from goose.goose import GOOSEPDU
from goose.goose_pdu import AllData
from goose.goose_pdu import Data
from goose.goose_pdu import IECGoosePDU
from goose.goose_pdu import UtcTime
from time import sleep


input_file = "goose.pcapng"
packets = rdpcap(input_file)
print("Read given pcap file"); sleep(2)
print("Processing Packets..."); sleep(1)

###############################
# Identify packets containing GOOSE messages.
###############################

GOOSE_TYPE = 0x88b8

def gooseTest(pkt):
    isGoose = False
    # Test for a Goose Ether Type
    if pkt.haslayer('Dot1Q'):
        if pkt['Dot1Q'].type == GOOSE_TYPE: isGoose = True
    if pkt.haslayer('Ether'):
        if pkt['Ether'].type == GOOSE_TYPE: isGoose = True
    return isGoose

# Filter packets based on source and destination MAC addresses
def filter_packets(pkt, src_mac, dst_mac):
    if pkt.haslayer(Ether):
        return pkt[Ether].src == src_mac and pkt[Ether].dst == dst_mac
    return False


# Process GOOSE PDU by decoding it with PYASN1
###############################
def goose_pdu_decode(encoded_data):

    g = IECGoosePDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassApplication,
            tag.tagFormatConstructed,
            1
        )
    )
    decoded_data, unprocessed_trail = decoder.decode(
        encoded_data,
        asn1Spec=g
    )
    # This should work, but not sure.
    return decoded_data



g_packets = []
src_mac = "00:02:a3:e0:c5:d2"  
dst_mac = "01:0c:cd:01:00:04" 



for p in packets:
    # Only process Goose Packets and filter by source and destination MAC addresses
    if gooseTest(p) and filter_packets(p, src_mac, dst_mac):
        # Store for processing later
        g_packets.append(p)


# print(len(g_packets))
# print(g_packets[0])

wrpcap('O1.pcap', g_packets)

#### take a random packet
import random
pnum = random.randint(0, len(g_packets))

print('\n\n')
print(f'Modifying packet-{pnum} from [ scr: {src_mac} --> dst: {dst_mac} ]')
print('\n\n')

#### Modify content of packet
# Get copy of packet and store the start and end of the payload
p = g_packets[pnum]
mod_p = p.copy()
mod_p_load_start = mod_p.load[:8]
mod_p_load_end = mod_p.load[-6:]

# Parse Goose Data
mod_d = GOOSE(mod_p.load)
mod_gpdu = mod_d[GOOSEPDU].original
mod_gd = goose_pdu_decode(mod_gpdu)

print('*'*20)
print("Original Packet")
print('*'*20)
print(mod_gd)

tmpT = Data()
tmpF = Data()
tmpT.setComponentByName('boolean', True)
tmpF.setComponentByName('boolean', False)

# Toggle Boolean Values
for e in range(mod_gd['numDatSetEntries']):
    if mod_gd['allData'].getComponentByPosition(e) == False:
        mod_gd['allData'].setComponentByPosition(e, tmpT)
        continue
    elif mod_gd['allData'].getComponentByPosition(e) == True:
        mod_gd['allData'].setComponentByPosition(e, tmpF)
        continue


print('*'*20)
print("Modified Packet")
print('*'*20)
print(mod_gd)


# Encode the modified data
en_gd = encoder.encode(mod_gd)

# Rebuild the packet payload
mod_p.load = mod_p_load_start + en_gd + mod_p_load_end

# wrpcap("O2.pcap", mod_p, append=True)

print('\n\n')
print('*'*20)
print(f"Successfully Modified packet-{pnum} !")
print('*'*20)


