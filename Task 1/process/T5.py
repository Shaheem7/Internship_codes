# !/usr/share/env python3

import os, sys, datetime, inspect, struct, time, argparse, pyshark
import numpy as np
from struct import *
from time import sleep
from copy import deepcopy
from warnings import filterwarnings
filterwarnings("ignore")

from pyasn1.codec.ber import decoder
from pyasn1.codec.ber import encoder
from pyasn1.type import char
from pyasn1.type import tag
from pyasn1.type import univ
from scapy.layers.l2 import Ether
from scapy.layers.l2 import Dot1Q
from scapy.compat import raw
from scapy.utils import hexdump
from scapy.utils import wrpcap
from scapy.all import rdpcap
from scapy.all import sendp

networkInterface = "eth1"
filter_string = "ether proto 0x88B8 and len <= 200"
GOOSE_TYPE = 0x88b8

# We have to tell script where to find the Goose module in parent directory

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from goose.goose import GOOSE
from goose.goose import GOOSEPDU
from goose.goose_pdu import AllData
from goose.goose_pdu import Data
from goose.goose_pdu import IECGoosePDU
from goose.goose_pdu import UtcTime




# CONVERTING THE TIME INTO 64-BITS or 8-BYTES FORM
UTC = 1 # 0: local time 1: UTC Time
def curTime64Bits(utc=False):
    # Microsecond Resolution Ignored
    if UTC:
        curTime = time.mktime(datetime.datetime.utcnow().timetuple())
    else:
        curTime = time.mktime(datetime.datetime.now().timetuple())

    curTimeInt = int(curTime)
    curTimeInt64 = (curTimeInt << 32)
    curTimeInt64Str = curTimeInt64.to_bytes(8,'big')
    return curTimeInt64Str


# This function will check whether the packets is a GOOSE packet or not
def goose_check(packet):
    isGoose = False
    # Test for a Goose Ether Type
    if packet.haslayer('Dot1Q'):
        if packet['Dot1Q'].type == GOOSE_TYPE: isGoose = True
    if packet.haslayer('Ether'):
        if packet['Ether'].type == GOOSE_TYPE: isGoose = True
    return isGoose

# This function will print all the ANS.1 decoded GOOSE PDU data 
def gooseASN1_DataPrint(data):
    print('\n\n')
    for field in list(IECGoosePDU()):
        if not data[field].hasValue():
            continue
        if type(data[field]) == char.VisibleString:
            print('%s: %s'%(field,str(data[field])))
            continue
        if type(data[field]) == univ.Integer:
            print('%s: %s'%(field,int(data[field])))
            continue
        if type(data[field]) == UtcTime:
            print('%s: %s'%(field,datetime.datetime.fromtimestamp(int.from_bytes(bytearray(data[field])[:4],'big')).strftime('%Y-%m-%d %H:%M:%S')))
            continue
        if type(data[field]) == univ.Boolean:
            print('%s: %s'%(field,str(data[field])))
            continue
        if type(data[field]) == AllData:
            print('%s'%(field))
            for field in data.getComponentByName('allData'):
                for value in field.values():
                    print('    %s'%(value))
            continue
        if type(data[field]) == univ.OctetString:
            print('%s: %s'%(field,str(data[field])))
            continue

# This function will decode the GOOSE PDU header using ASN.1 decoding 
def gooseAllData_decode(encoded_data):
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

    return decoded_data


### PARSING THE GOOSE AND GOOSE PDU HEADERS ###

packets = rdpcap('goose.pcapng')

print("[+] Parsing GOOSE header and GOOSE PDU header"); sleep(1)
print("[+] Decoding the GOOSE PDU header"); sleep(1)


unique_src = []
unique_dst = []
unique_mac_pairs = set

datSetList = []
g_packets = []
for packet in packets:
    if goose_check(packet):
        # Appending/Storing the packets into a array/list
        g_packets.append(packet)
        
        if packet.haslayer(Ether):
            unique_src.append(packet[Ether].src)
            unique_dst.append(packet[Ether].dst)
            unique_mac_pairs.add((packet[Ether].src, packet[Ether].dst))

        # Parse the GOOSE header and GOOSE PDU header
        data = GOOSE(packet.load)

        # Grab the Goose PDU for processing
        goose_pdu = data[GOOSEPDU].original

        # Use PYASN1 to parse the Goose PDU
        goose_decoded = gooseAllData_decode(goose_pdu)

        # Creating a list of datSet
        datSetList.append(str(goose_decoded['datSet']))
        
        
print(len(datSetList))

print(datSetList[0:5])

print(len(unique_src))
print(len(unique_dst))
print(unique_mac_pairs)
