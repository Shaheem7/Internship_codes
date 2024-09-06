import pyshark

# Path to your pcap file
input_pcap = 'Supervised_200.pcap'

# Capture the packets from the pcap file
capture = pyshark.FileCapture(input_pcap)

# Iterate through each packet in the capture
for packet in capture:
    print(f"Packet Number: {packet.number}")
    print(f"Source IP: {packet.ip.src}")
    print(f"Destination IP: {packet.ip.dst}")
    print("Layers:")
    
    # Print all layers in the packet
    for layer in packet.layers:
        print(f" - Layer: {layer.layer_name}")
        print(f"   Layer Details: {layer}")
    
    print("\n" + "="*50 + "\n")

capture.close()
