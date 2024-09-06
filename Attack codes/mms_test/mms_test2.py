from pyasn1.codec.ber import decoder
from pyasn1.type import univ, namedtype, tag, constraint, char, useful

from mms import Confirmed_ResponsePDU, Confirmed_RequestPDU

from scapy.all import *

from pyasn1 import debug
debug.setLogger(debug.Debug('all'))




def decode_Confirmed_RequestPDU(encoded_data):
    conf_req = Confirmed_RequestPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassUniversal,    # Universal tag class
            tag.tagFormatSimple,      # Primitive tag format
            0                        # Identifier 0 (adjust if needed)
        )
    )
    
    try:
        decoded_conf_req, rest_of_data = decoder.decode(
            encoded_data,
            asn1Spec=conf_req
        )
        print(f"Decoded Confirmed Request PDU: {decoded_conf_req.prettyPrint()}")
        return decoded_conf_req
    except Exception as e:
        print(f"Decoding error: {e}")
        print(f"Data being decoded: {encoded_data}")
        return None


file = "ABB1.pcap"
packets = rdpcap(file)

pkt = packets[3]

# Decoding the packet
raw_data = pkt.load
print(f"Raw Data : {raw_data}")

other_headers = 4+3+2+2+9   + 2

mms_data = raw_data[other_headers:]
print(f"MMS Data: {mms_data}")


decoded_req_pdu = decode_Confirmed_RequestPDU(mms_data)
# invokeID = decoded_req_pdu.getComponentByPosition(0)



# decoded_res_pdu = decode_Confirmed_ResponsePDU(mms_data)
# invokeID = decoded_res_pdu.getComponentByPosition(0)


# print(f'invokeID = {invokeID}')

