
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


input_file = "goose.pcapng"
packets = rdpcap(input_file)


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


# Process packets and search for GOOSE
###############################

g_packets = []
for p in packets:
    # Only process Goose Packets
    if gooseTest(p):
        # Store for processing later
        g_packets.append(p)




#### packets to modify
pnum = 1100


#### Modify content

# Get copy of packet and store the start and end of the payload
p                = g_packets[pnum]
mod_p            = p.copy()
mod_p_load_start = mod_p.load[:8]
mod_p_load_end   = mod_p.load[-6:]


# Parse Goose Data
mod_d    = GOOSE(mod_p.load)
mod_gpdu = mod_d[GOOSEPDU].original
mod_gd   = goose_pdu_decode(mod_gpdu)

print(mod_gd)



tmpT = Data()
tmpF = Data()
tmpT.setComponentByName('boolean',True)
tmpF.setComponentByName('boolean',False)

# Toggle Boolean Values
for e in range(mod_gd['numDatSetEntries']):
    if mod_gd['allData'].getComponentByPosition(e) == False:
        mod_gd['allData'].setComponentByPosition(e,tmpT)
        continue
    elif mod_gd['allData'].getComponentByPosition(e) == True:
        mod_gd['allData'].setComponentByPosition(e,tmpF)
        continue

print(mod_gd)


# Encode the modified data
en_gd = encoder.encode(mod_gd)


# Rebuild the packet payload
mod_p.load = mod_p_load_start + en_gd + mod_p_load_end

wrpcap("code1.pcap", mod_p, append=True)


