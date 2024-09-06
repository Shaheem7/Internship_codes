from scapy.all import *
from pyasn1.codec.ber import decoder, encoder
from pyasn1.error import PyAsn1Error
from mms import Confirmed_RequestPDU

# Function to parse MMS packet and modify invoke ID
def modify_invoke_id(mms_packet, new_invoke_id):
    # Extract MMS PDU from packet payload (assuming it is MMS)
    raw_data = bytes(mms_packet.payload)

    try:
        # Decode the MMS PDU
        pdu, _ = decoder.decode(raw_data, asn1Spec=Confirmed_RequestPDU())
        
        # Modify the invoke ID if present
        if 'invokeID' in pdu:
            pdu.setComponentByName('invokeID', new_invoke_id)
        
        # Re-encode the modified PDU
        modified_pdu = encoder.encode(pdu)
        
        # Rebuild the packet with modified payload
        mms_packet.payload = Raw(modified_pdu)
    
    except PyAsn1Error as e:
        print(f"ASN.1 decoding error: {e}")
        print(f"Raw data: {raw_data}")
        print("Attempting with another PDU format...")
        # Try other PDU formats or check tags
        
    return mms_packet


# Example usage:
# Read the MMS packet from a pcap file or capture it live
mms_packet = rdpcap('ABB1.pcap')[2]  # assuming first packet is MMS

# Modify the invoke ID to 12345
new_invoke_id = 12345
modified_packet = modify_invoke_id(mms_packet, new_invoke_id)

# Save or send the modified packet
wrpcap('modified_mms.pcap', modified_packet)
