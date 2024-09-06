from pyasn1.type import univ, char, namedtype, namedval, tag, constraint, useful


class Unsigned32(univ.Integer):
    pass



class Confirmed_RequestPDU(univ.Sequence):
    pass


Confirmed_RequestPDU.componentType = namedtype.NamedTypes(
    namedtype.NamedType('invokeID', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))) #,
    # namedtype.OptionalNamedType('listOfModifier', univ.SequenceOf(componentType=Modifier())),
    # namedtype.NamedType('confirmedServiceRequest', ConfirmedServiceRequest().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))   # ,
    # namedtype.OptionalNamedType('cs-request-detail', CS_Request_Detail().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 79)))
)

