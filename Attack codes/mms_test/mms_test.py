from pyasn1.codec.ber import decoder
from pyasn1.type import univ, namedtype, tag, constraint, char, useful

# from mms import Confirmed_ResponsePDU, Confirmed_RequestPDU
from mms_t import Confirmed_RequestPDU


from scapy.all import *

from pyasn1 import debug
debug.setLogger(debug.Debug('all'))

# Decode the packet
def decode_Confirmed_RequestPDU(encoded_data):
    conf_req = Confirmed_RequestPDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassUniversal,
            tag.tagFormatSimple,
            2
        )
    )
    
    decoded_conf_req, rest_of_data = decoder.decode(
        encoded_data,
        asn1Spec=conf_req
    )
    
    return decoded_conf_req

# def decode_Confirmed_ResponsePDU(encoded_data):
#     conf_res = Confirmed_ResponsePDU().subtype(
#         implicitTag=tag.Tag(
#             tag.tagClassUniversal,
#             tag.tagFormatSimple,
#             2
#         )
#     )
    
#     decoded_conf_res, rest_of_data = decoder.decode(
#         encoded_data,
#         asn1Spec=conf_res
#     )
    
#     return decoded_conf_res



file = "ABB2.pcap"
packets = rdpcap(file)

pkt = packets[2]

# Decoding the packet
raw_data = pkt.load
print(f"Raw Data : {raw_data}")

other_headers = 4+3+2+2+9   + 2

mms_data = raw_data[other_headers:]
print(f"MMS Data: {mms_data}")







decoded_req_pdu = decode_Confirmed_RequestPDU(mms_data)
invokeID = decoded_req_pdu.getComponentByPosition(0)



# decoded_res_pdu = decode_Confirmed_ResponsePDU(mms_data)
# invokeID = decoded_res_pdu.getComponentByPosition(0)


# print(f'invokeID = {invokeID}')


