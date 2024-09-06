# (last modified on 2024-08-28 16:56:39.390085)  

# MMS
from pyasn1.type import univ, char, namedtype, namedval, tag, constraint, useful


class DataAccessError(univ.Integer):
    pass


DataAccessError.namedValues = namedval.NamedValues(
    ('object-invalidated', 0),
    ('hardware-fault', 1),
    ('temporarily-unavailable', 2),
    ('object-access-denied', 3),
    ('object-undefined', 4),
    ('invalid-address', 5),
    ('type-unsupported', 6),
    ('type-inconsistent', 7),
    ('object-attribute-inconsistent', 8),
    ('object-access-unsupported', 9),
    ('object-non-existent', 10)
)


class FloatingPoint(univ.OctetString):
    pass


class TimeOfDay(univ.OctetString):
    pass


class UtcTime(univ.OctetString):
    pass


class MMSString(char.UTF8String):
    pass


class Data(univ.Choice):
    pass


Data.componentType = namedtype.NamedTypes(
    namedtype.NamedType('array', univ.SequenceOf(componentType=Data()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('structure', univ.SequenceOf(componentType=Data()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.NamedType('boolean', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),        
    namedtype.NamedType('bit-string', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),   
    namedtype.NamedType('integer', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),        
    namedtype.NamedType('unsigned', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),       
    namedtype.NamedType('floating-point', FloatingPoint().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),    namedtype.NamedType('octet-string', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 9))),
    namedtype.NamedType('visible-string', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 10))),
    namedtype.NamedType('binary-time', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 12))),      
    namedtype.NamedType('bcd', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 13))),
    namedtype.NamedType('booleanArray', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 14))),    namedtype.NamedType('objId', univ.ObjectIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 15))),    namedtype.NamedType('mMSString', MMSString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 16))),        
    namedtype.NamedType('utc-time', UtcTime().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 17)))
)


class AccessResult(univ.Choice):
    pass


AccessResult.componentType = namedtype.NamedTypes(
    namedtype.NamedType('failure', DataAccessError().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),     
    namedtype.NamedType('success', Data())
)


class Identifier(char.VisibleString):
    pass


class ObjectName(univ.Choice):
    pass


ObjectName.componentType = namedtype.NamedTypes(
    namedtype.NamedType('vmd-specific', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),     
    namedtype.NamedType('domain-specific', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('domainId', Identifier()),
        namedtype.NamedType('itemId', Identifier())
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('aa-specific', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))       
)


class Unsigned32(univ.Integer):
    pass


class EventTime(univ.Choice):
    pass


EventTime.componentType = namedtype.NamedTypes(
    namedtype.NamedType('timeOfDayT', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),        
    namedtype.NamedType('timeSequenceIdentifier', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class EC_State(univ.Integer):
    pass


EC_State.namedValues = namedval.NamedValues(
    ('disabled', 0),
    ('idle', 1),
    ('active', 2)
)


class AcknowledgeEventNotification_Request(univ.Sequence):
    pass


AcknowledgeEventNotification_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('acknowledgedState', EC_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),  
    namedtype.NamedType('timeOfAcknowledgedTransition', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3)))
)


class AcknowledgeEventNotification_Response(univ.Null):
    pass


class Address(univ.Choice):
    pass


Address.componentType = namedtype.NamedTypes(
    namedtype.NamedType('numericAddress', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.NamedType('symbolicAddress', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('unconstrainedAddress', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class AlarmAckRule(univ.Integer):
    pass


AlarmAckRule.namedValues = namedval.NamedValues(
    ('none', 0),
    ('simple', 1),
    ('ack-active', 2),
    ('ack-all', 3)
)


class EE_State(univ.Integer):
    pass


EE_State.namedValues = namedval.NamedValues(
    ('disabled', 0),
    ('idle', 1),
    ('active', 2),
    ('activeNoAckA', 3),
    ('idleNoAckI', 4),
    ('idleNoAckA', 5),
    ('idleAcked', 6),
    ('activeAcked', 7)
)


class ApplicationReference(univ.Sequence):
    pass


ApplicationReference.componentType = namedtype.NamedTypes(

)


class Unsigned8(univ.Integer):
    pass


class AlarmEnrollmentSummary(univ.Sequence):
    pass


AlarmEnrollmentSummary.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('clientApplication', ApplicationReference().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.NamedType('severity', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('currentState', EC_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),       
    namedtype.DefaultedNamedType('notificationLost', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6)).subtype(value=0)),
    namedtype.OptionalNamedType('alarmAcknowledgmentRule', AlarmAckRule().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
    namedtype.OptionalNamedType('enrollementState', EE_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))),
    namedtype.OptionalNamedType('timeOfLastTransitionToActive', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 9))),
    namedtype.OptionalNamedType('timeActiveAcknowledged', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 10))),
    namedtype.OptionalNamedType('timeOfLastTransitionToIdle', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 11))),
    namedtype.OptionalNamedType('timeIdleAcknowledged', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 12)))
)


class AlarmSummary(univ.Sequence):
    pass


AlarmSummary.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('severity', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('currentState', EC_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),       
    namedtype.NamedType('unacknowledgedState', univ.Integer(namedValues=namedval.NamedValues(('none', 0), ('active', 1), ('idle', 2), ('both', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.OptionalNamedType('timeOfLastTransitionToActive', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5))),
    namedtype.OptionalNamedType('timeOfLastTransitionToIdle', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6)))
)


class Priority(Unsigned8):
    pass


class AlterEventConditionMonitoring_Request(univ.Sequence):
    pass


AlterEventConditionMonitoring_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('enabled', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),    namedtype.OptionalNamedType('priority', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),   
    namedtype.OptionalNamedType('alarmSummaryReports', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.OptionalNamedType('evaluationInterval', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))
)


class AlterEventConditionMonitoring_Response(univ.Null):
    pass


class Transitions(univ.BitString):
    pass


Transitions.namedValues = namedval.NamedValues(
    ('idle-to-disabled', 0),
    ('active-to-disabled', 1),
    ('disabled-to-idle', 2),
    ('active-to-idle', 3),
    ('disabled-to-active', 4),
    ('idle-to-active', 5),
    ('any-to-deleted', 6)
)


class AlterEventEnrollment_Request(univ.Sequence):
    pass


AlterEventEnrollment_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('eventConditionTransitions', Transitions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('alarmAcknowledgmentRule', AlarmAckRule().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class AlterEventEnrollment_Response(univ.Sequence):
    pass


AlterEventEnrollment_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('currentState', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('state', EE_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('undefined', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))      
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('transitionTime', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))


class AlternateAccessSelection(univ.Choice):
    pass


class AlternateAccess(univ.SequenceOf):
    pass


AlternateAccessSelection.componentType = namedtype.NamedTypes(
    namedtype.NamedType('selectAlternateAccess', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('accessSelection', univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('component', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),            namedtype.NamedType('index', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),    
            namedtype.NamedType('indexRange', univ.Sequence(componentType=namedtype.NamedTypes(
                namedtype.NamedType('lowIndex', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType('numberOfElements', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
            ))
            .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
            namedtype.NamedType('allElements', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)))        ))
        ),
        namedtype.NamedType('alternateAccess', AlternateAccess())
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('selectAccess', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('component', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),    
        namedtype.NamedType('index', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),        
        namedtype.NamedType('indexRange', univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('lowIndex', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), 
            namedtype.NamedType('nmberOfElements', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
        ))
        .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
        namedtype.NamedType('allElements', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))    
    ))
    )
)


AlternateAccess.componentType = univ.Choice(componentType=namedtype.NamedTypes(
    namedtype.NamedType('unnamed', AlternateAccessSelection()),
    namedtype.NamedType('named', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('componentName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),        namedtype.NamedType('accesst', AlternateAccessSelection())
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
))


class AttachToEventCondition(univ.Sequence):
    pass


AttachToEventCondition.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('causingTransitions', Transitions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('acceptableDelay', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)))
)


class AttachToSemaphore(univ.Sequence):
    pass


AttachToSemaphore.componentType = namedtype.NamedTypes(
    namedtype.NamedType('semaphoreName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('namedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.DefaultedNamedType('priority', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=64)),
    namedtype.OptionalNamedType('acceptableDelay', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.OptionalNamedType('controlTimeOut', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
    namedtype.OptionalNamedType('abortOnTimeOut', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
    namedtype.DefaultedNamedType('relinquishIfConnectionLost', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6)).subtype(value=1))
)


class CS_Request_Detail(univ.Choice):
    pass


CS_Request_Detail.componentType = namedtype.NamedTypes(
    namedtype.NamedType('foo', univ.Integer())
)


class ProgramInvocationState(univ.Integer):
    pass


ProgramInvocationState.namedValues = namedval.NamedValues(
    ('non-existent', 0),
    ('unrunable', 1),
    ('idle', 2),
    ('running', 3),
    ('stopped', 4),
    ('starting', 5),
    ('stopping', 6),
    ('resuming', 7),
    ('resetting', 8)
)


class Stop_Error(ProgramInvocationState):
    pass


class Start_Error(ProgramInvocationState):
    pass


class DeleteNamedVariableList_Error(Unsigned32):
    pass


class ObtainFile_Error(univ.Integer):
    pass


ObtainFile_Error.namedValues = namedval.NamedValues(
    ('source-file', 0),
    ('destination-file', 1)
)


class DeleteVariableAccess_Error(Unsigned32):
    pass


class DefineEventEnrollment_Error(ObjectName):
    pass


class FileRename_Error(univ.Integer):
    pass


FileRename_Error.namedValues = namedval.NamedValues(
    ('source-file', 0),
    ('destination-file', 1)
)


class Resume_Error(ProgramInvocationState):
    pass


class DeleteNamedType_Error(Unsigned32):
    pass


class Reset_Error(ProgramInvocationState):
    pass


class ServiceError(univ.Sequence):
    pass


ServiceError.componentType = namedtype.NamedTypes(
    namedtype.NamedType('errorClass', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('vmd-state', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('vmd-state-conflict', 1), ('vmd-operational-problem', 2), ('domain-transfer-problem', 3), ('state-machine-id-invalid', 4))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('application-reference', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('aplication-unreachable', 1), ('connection-lost', 2), ('application-reference-invalid', 3), ('context-unsupported', 4))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('definition', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('object-undefined', 1), ('invalid-address', 2), ('type-unsupported', 3), ('type-inconsistent', 4), ('object-exists', 5), ('object-attribute-inconsistent', 6))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
        namedtype.NamedType('resource', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('memory-unavailable', 1), ('processor-resource-unavailable', 2), ('mass-storage-unavailable', 3), ('capability-unavailable', 4), ('capability-unknown', 5))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
        namedtype.NamedType('service', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('primitives-out-of-sequence', 1), ('object-sate-conflict', 2), ('pdu-size', 3), ('continuation-invalid', 4), ('object-constraint-conflict', 5))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
        namedtype.NamedType('service-preempt', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('timeout', 1), ('deadlock', 2), ('cancel', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
        namedtype.NamedType('time-resolution', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('unsupportable-time-resolution', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
        namedtype.NamedType('access', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('object-access-unsupported', 1), ('object-non-existent', 2), ('object-access-denied', 3), ('object-invalidated', 4))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
        namedtype.NamedType('initiate', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('version-incompatible', 1), ('max-segment-insufficient', 2), ('max-services-outstanding-calling-insufficient', 3), ('max-services-outstanding-called-insufficient', 4), ('service-CBB-insufficient', 5), ('parameter-CBB-insufficient', 6), ('nesting-level-insufficient', 7))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))),
        namedtype.NamedType('conclude', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('further-communication-required', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 9))),
        namedtype.NamedType('cancel', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invoke-id-unknown', 1), ('cancel-not-possible', 2))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 10))),
        namedtype.NamedType('file', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('filename-ambiguous', 1), ('file-busy', 2), ('filename-syntax-error', 3), ('content-type-invalid', 4), ('position-invalid', 5), ('file-acces-denied', 6), ('file-non-existent', 7), ('duplicate-filename', 8), ('insufficient-space-in-filestore', 9))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 11))),
        namedtype.NamedType('others', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 12)))     
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('additionalCode', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('additionalDescription', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('serviceSpecificInformation', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('obtainFile', ObtainFile_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('start', Start_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),       
        namedtype.NamedType('stop', Stop_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
        namedtype.NamedType('resume', Resume_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),     
        namedtype.NamedType('reset', Reset_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),       
        namedtype.NamedType('deleteVariableAccess', DeleteVariableAccess_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
        namedtype.NamedType('deleteNamedVariableList', DeleteNamedVariableList_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
        namedtype.NamedType('deleteNamedType', DeleteNamedType_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
        namedtype.NamedType('defineEventEnrollment-Error', DefineEventEnrollment_Error().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 8))),
        namedtype.NamedType('fileRename', FileRename_Error().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 9)))
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3)))
)


class Cancel_ErrorPDU(univ.Sequence):
    pass


Cancel_ErrorPDU.componentType = namedtype.NamedTypes(
    namedtype.NamedType('originalInvokeID', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), 
    namedtype.NamedType('serviceError', ServiceError().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class Cancel_RequestPDU(Unsigned32):
    pass


class Cancel_ResponsePDU(Unsigned32):
    pass


class Conclude_ErrorPDU(ServiceError):
    pass


class Conclude_RequestPDU(univ.Null):
    pass


class Conclude_ResponsePDU(univ.Null):
    pass


class Confirmed_ErrorPDU(univ.Sequence):
    pass


Confirmed_ErrorPDU.componentType = namedtype.NamedTypes(
    namedtype.NamedType('invokeID', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.OptionalNamedType('modifierPosition', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('serviceError', ServiceError().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class Modifier(univ.Choice):
    pass


Modifier.componentType = namedtype.NamedTypes(
    namedtype.NamedType('attach-To-Event-Condition', AttachToEventCondition().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('attach-To-Semaphore', AttachToSemaphore().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class GetEventActionAttributes_Request(ObjectName):
    pass


class GetScatteredAccessAttributes_Request(ObjectName):
    pass


class DeleteEventEnrollment_Request(univ.Choice):
    pass


DeleteEventEnrollment_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('specific', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('ec', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('ea', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class FileName(univ.SequenceOf):
    pass


FileName.componentType = char.GraphicString()


class LoadDomainContent_Request(univ.Sequence):
    pass


LoadDomainContent_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.OptionalNamedType('listOfCapabilities', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('sharable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),       
    namedtype.NamedType('fileName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
    namedtype.OptionalNamedType('thirdParty', ApplicationReference().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
)


class TerminateDownloadSequence_Request(univ.Sequence):
    pass


TerminateDownloadSequence_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.OptionalNamedType('discard', ServiceError().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class DeleteJournal_Request(univ.Sequence):
    pass


DeleteJournal_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('journalName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0)))  
)


class JOU_Additional_Detail(univ.Null):
    pass


class EntryContent(univ.Sequence):
    pass


EntryContent.componentType = namedtype.NamedTypes(
    namedtype.NamedType('occurenceTime', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),     
    namedtype.OptionalNamedType('additionalDetail', JOU_Additional_Detail().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('entryForm', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('data', univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.OptionalNamedType('event', univ.Sequence(componentType=namedtype.NamedTypes(
                namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
                namedtype.NamedType('currentState', EC_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)))
            ))
            .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
            namedtype.OptionalNamedType('listOfVariables', univ.SequenceOf(componentType=univ.Sequence(componentType=namedtype.NamedTypes(
                namedtype.NamedType('variableTag', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
                namedtype.NamedType('valueSpecification', Data().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
            ))
            ).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
        ))
        .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
        namedtype.NamedType('annotation', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
3)))
    ))
    )
)


class WriteJournal_Request(univ.Sequence):
    pass


WriteJournal_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('journalName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), 
    namedtype.NamedType('listOfJournalEntry', univ.SequenceOf(componentType=EntryContent()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class InitializeJournal_Request(univ.Sequence):
    pass


InitializeJournal_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('journalName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), 
    namedtype.OptionalNamedType('limitSpecification', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('limitingTime', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),  
        namedtype.OptionalNamedType('limitingEntry', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class DownloadSegment_Request(Identifier):
    pass


class CreateProgramInvocation_Request(univ.Sequence):
    pass


CreateProgramInvocation_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('programInvocationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('listOfDomainName', univ.SequenceOf(componentType=Identifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.DefaultedNamedType('reusable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=1)),
    namedtype.OptionalNamedType('monitorType', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)))
)


class DeleteEventCondition_Request(univ.Choice):
    pass


DeleteEventCondition_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('specific', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('aa-specific', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),       
    namedtype.NamedType('domain', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.NamedType('vmd', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)))
)


class Resume_Request(univ.Sequence):
    pass


Resume_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('programInvocationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.OptionalNamedType('executionArgument', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('simpleString', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        # namedtype.NamedType('encodedString', EXTERNALt())
    ))
    )
)


class ReportSemaphoreStatus_Request(ObjectName):
    pass


class Stop_Request(univ.Sequence):
    pass


Stop_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('programInvocationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
)


class DefineEventAction_Request(univ.Sequence):
    pass


DefineEventAction_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventActionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('listOfModifier', univ.SequenceOf(componentType=Modifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class GetEventConditionAttributes_Request(ObjectName):
    pass


class FileDirectory_Request(univ.Sequence):
    pass


FileDirectory_Request.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('fileSpecification', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.OptionalNamedType('continueAfter', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class GetNamedTypeAttributes_Request(ObjectName):
    pass


class StoreDomainContent_Request(univ.Sequence):
    pass


StoreDomainContent_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.NamedType('filenName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('thirdParty', ApplicationReference().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class Integer32(univ.Integer):
    pass


class TerminateUploadSequence_Request(Integer32):
    pass


class FileClose_Request(Integer32):
    pass


class RelinquishControl_Request(univ.Sequence):
    pass


RelinquishControl_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('semaphoreName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('namedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))


class ReportJournalStatus_Request(ObjectName):
    pass


class GetAlarmEnrollmentSummary_Request(univ.Sequence):
    pass


GetAlarmEnrollmentSummary_Request.componentType = namedtype.NamedTypes(
    namedtype.DefaultedNamedType('enrollmentsOnly', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=1)),
    namedtype.DefaultedNamedType('activeAlarmsOnly', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value=1)),
    # namedtype.DefaultedNamedType('acknowledgmentFilter', univ.Integer(namedValues=namedval.NamedValues(('not-acked', 0), ('acked', 1), ('all', 2))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=not_acked)),
    namedtype.OptionalNamedType('severityFilter', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('mostSevere', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
        namedtype.NamedType('leastSevere', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))    
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
    namedtype.OptionalNamedType('continueAfter', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
)


class TypeSpecification(univ.Choice):
    pass


TypeSpecification.componentType = namedtype.NamedTypes(
    namedtype.NamedType('typeName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),    
    namedtype.NamedType('array', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.DefaultedNamedType('packed', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)),
        namedtype.NamedType('numberOfElements', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('elementType', TypeSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('structure', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.DefaultedNamedType('packed', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)),
        namedtype.NamedType('components', univ.SequenceOf(componentType=univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.OptionalNamedType('componentName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
            namedtype.NamedType('componentType', TypeSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
        ))
        ).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.NamedType('boolean', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('bit-string', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),        
    namedtype.NamedType('integer', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
    namedtype.NamedType('unsigned', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
    namedtype.NamedType('octet-string', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 9))),      
    namedtype.NamedType('visible-string', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 10))),   
    namedtype.NamedType('generalized-time', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 11))), 
    namedtype.NamedType('binary-time', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 12))),   
    namedtype.NamedType('bcd', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 13))),
    namedtype.NamedType('objId', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 15)))
)


class ScatteredAccessDescription(univ.SequenceOf):
    pass


class VariableSpecification(univ.Choice):
    pass


ScatteredAccessDescription.componentType = univ.Sequence(componentType=namedtype.NamedTypes(
    namedtype.OptionalNamedType('componentName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('variableSpecification', VariableSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.OptionalNamedType('alternateAccess', AlternateAccess().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
))


VariableSpecification.componentType = namedtype.NamedTypes(
    namedtype.NamedType('name', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),        
    namedtype.NamedType('address', Address().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),        
    namedtype.NamedType('variableDescription', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('address', Address()),
        namedtype.NamedType('typeSpecification', TypeSpecification())
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.NamedType('scatteredAccessDescription', ScatteredAccessDescription().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('invalidated', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))        
)


class EC_Class(univ.Integer):
    pass


EC_Class.namedValues = namedval.NamedValues(
    ('network-triggered', 0),
    ('monitored', 1)
)


class DefineEventCondition_Request(univ.Sequence):
    pass


DefineEventCondition_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('class', EC_Class().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.DefaultedNamedType('prio-rity', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=64)),
    namedtype.DefaultedNamedType('severity', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)).subtype(value=64)),
    namedtype.OptionalNamedType('alarmSummaryReports', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
    namedtype.OptionalNamedType('monitoredVariable', VariableSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6))),
    namedtype.OptionalNamedType('evaluationInterval', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7)))
)


class GetCapabilityList_Request(univ.Sequence):
    pass


GetCapabilityList_Request.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('continueAfter', char.VisibleString())
)


class GetNameList_Request(univ.Sequence):
    pass


GetNameList_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('extendedObjectClass', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('objectClass', univ.Integer(namedValues=namedval.NamedValues(('nammedVariable', 0), ('scatteredAccess', 1), ('namedVariableList', 2), ('namedType', 3), ('semaphore', 4), ('eventCondition', 5), ('eventAction', 6), ('eventEnrollment', 7), ('journal', 8), ('domain', 9), ('programInvocation', 10), ('operatorStation', 11))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('objectScope', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('vmdSpecific', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
        namedtype.NamedType('domainSpecific', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('aaSpecific', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))     
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.OptionalNamedType('continueAfter', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class GetAlarmSummary_Request(univ.Sequence):
    pass


GetAlarmSummary_Request.componentType = namedtype.NamedTypes(
    namedtype.DefaultedNamedType('enrollmentsOnly', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=1)),
    namedtype.DefaultedNamedType('activeAlarmsOnly', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value=1)),
    # namedtype.DefaultedNamedType('acknowledgmentFilter', univ.Integer(namedValues=namedval.NamedValues(('not-acked', 0), ('acked', 1), ('all', 2))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=not_acked)),
    namedtype.OptionalNamedType('severityFilter', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('mostSevere', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
        namedtype.NamedType('leastSevere', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))    
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
    namedtype.OptionalNamedType('continueAfter', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
)


class ReportEventActionStatus_Request(ObjectName):
    pass


class ReportEventConditionStatus_Request(ObjectName):
    pass


class ReportPoolSemaphoreStatus_Request(univ.Sequence):
    pass


ReportPoolSemaphoreStatus_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('semaphoreName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('nameToStartAfter', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class RequestDomainDownload_Request(univ.Sequence):
    pass


RequestDomainDownload_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.OptionalNamedType('listOfCapabilities', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('sharable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),       
    namedtype.NamedType('fileName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))
)


class VariableAccessSpecification(univ.Choice):
    pass


VariableAccessSpecification.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfVariable', univ.SequenceOf(componentType=univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('variableSpecification', VariableSpecification()),
        namedtype.OptionalNamedType('alternateAccess', AlternateAccess().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5)))
    ))
    ).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('variableListName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class Read_Request(univ.Sequence):
    pass


Read_Request.componentType = namedtype.NamedTypes(
    namedtype.DefaultedNamedType('specificationWithResult', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)),
    namedtype.NamedType('variableAccessSpecificatn', VariableAccessSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class FileOpen_Request(univ.Sequence):
    pass


FileOpen_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('fileName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('initialPosition', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))   
)


class ReadJournal_Request(univ.Sequence):
    pass


ReadJournal_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('journalName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), 
    namedtype.OptionalNamedType('rangeStartSpecification', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('startingTime', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),  
        namedtype.NamedType('startingEntry', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.OptionalNamedType('rangeStopSpecification', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('endingTime', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
        namedtype.NamedType('numberOfEntries', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.OptionalNamedType('listOfVariables', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
    namedtype.NamedType('entryToStartAfter', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('timeSpecification', TimeOfDay().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('entrySpecification', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
)


class Write_Request(univ.Sequence):
    pass


Write_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('variableAccessSpecificatn', VariableAccessSpecification()),
    namedtype.NamedType('listOfData', univ.SequenceOf(componentType=Data()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
)


class ObtainFile_Request(univ.Sequence):
    pass


ObtainFile_Request.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('sourceFileServer', ApplicationReference().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('sourceFile', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('destinationFile', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))     
)


class FileRead_Request(Integer32):
    pass


class DefineEventEnrollment_Request(univ.Sequence):
    pass


DefineEventEnrollment_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('eventConditionTransition', Transitions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.NamedType('alarmAcknowledgementRule', AlarmAckRule().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.OptionalNamedType('eventActionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))),
    namedtype.OptionalNamedType('clientApplication', ApplicationReference().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
)


class Start_Request(univ.Sequence):
    pass


Start_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('programInvocationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.OptionalNamedType('executionArgument', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('simpleString', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        # namedtype.NamedType('encodedString', EXTERNALt())
    ))
    )
)


class Rename_Request(univ.Sequence):
    pass


Rename_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('extendedObjectClass', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('objectClass', univ.Integer(namedValues=namedval.NamedValues(('namedVariable', 0), ('scatteredAccess', 1), ('namedVariableList', 2), ('namedType', 3), ('semaphore', 4), ('eventCondition', 5), ('eventAction', 6), ('eventEnrollment', 7), ('journal', 8), ('domain', 9), ('programInvocation', 10), ('operatorStation', 11))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('currentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), 
    namedtype.NamedType('newIdentifier', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))     
)


class UploadSegment_Request(Integer32):
    pass


class DeleteNamedType_Request(univ.Sequence):
    pass


DeleteNamedType_Request.componentType = namedtype.NamedTypes(
#     namedtype.DefaultedNamedType('scopeOfDelete', univ.Integer(namedValues=namedval.NamedValues(('specific', 0), ('aa-specific', 1), 
# ('domain', 2), ('vmd', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=specific)),      
    namedtype.OptionalNamedType('listOfTypeName', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))


class Input_Request(univ.Sequence):
    pass


Input_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('operatorStationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('echo', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value=1)),
    namedtype.OptionalNamedType('listOfPromptData', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('inputTimeOut', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)))
)


class Status_Request(univ.Boolean):
    pass


class InitiateDownloadSequence_Request(univ.Sequence):
    pass


InitiateDownloadSequence_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.NamedType('listOfCapabilities', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('sharable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))        
)


class DefineScatteredAccess_Request(univ.Sequence):
    pass


DefineScatteredAccess_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('scatteredAccessName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('scatteredAccessDescription', ScatteredAccessDescription().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class GetEventEnrollmentAttributes_Request(univ.Sequence):
    pass


GetEventEnrollmentAttributes_Request.componentType = namedtype.NamedTypes(
    # namedtype.DefaultedNamedType('scopeOfRequest', univ.Integer(namedValues=namedval.NamedValues(('specific', 0), ('client', 1), ('ec', 2), ('ea', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=client)),
    namedtype.OptionalNamedType('eventEnrollmentNames', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('clientApplication', ApplicationReference().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.OptionalNamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
    namedtype.OptionalNamedType('eventActionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))),
    namedtype.OptionalNamedType('continueAfter', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5)))
)


class GetNamedVariableListAttributes_Request(ObjectName):
    pass


class ReportSemaphoreEntryStatus_Request(univ.Sequence):
    pass


ReportSemaphoreEntryStatus_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('semaphoreName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('state', univ.Integer(namedValues=namedval.NamedValues(('queued', 0), ('owner', 1), ('hung', 2))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('entryIdToStartAfter', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class FileDelete_Request(FileName):
    pass


class Output_Request(univ.Sequence):
    pass


Output_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('operatorStationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('listOfOutputData', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class DeleteNamedVariableList_Request(univ.Sequence):
    pass


DeleteNamedVariableList_Request.componentType = namedtype.NamedTypes(
#     namedtype.DefaultedNamedType('scopeOfDelete', univ.Integer(namedValues=namedval.NamedValues(('specific', 0), ('aa-specific', 1), 
# ('domain', 2), ('vmd', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=specific)),      
    namedtype.OptionalNamedType('listOfVariableListName', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))


class Identify_Request(univ.Null):
    pass


class DeleteProgramInvocation_Request(Identifier):
    pass


class ReportEventEnrollmentStatus_Request(ObjectName):
    pass


class FileRename_Request(univ.Sequence):
    pass


FileRename_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('currentFileName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
    namedtype.NamedType('newFileName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class DefineNamedVariable_Request(univ.Sequence):
    pass


DefineNamedVariable_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('variableName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),    namedtype.NamedType('address', Address().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),        
    namedtype.OptionalNamedType('typeSpecification', TypeSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class RequestDomainUpload_Request(univ.Sequence):
    pass


RequestDomainUpload_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.NamedType('fileName', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class Reset_Request(univ.Sequence):
    pass


Reset_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('programInvocationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
)


class GetProgramInvocationAttributes_Request(Identifier):
    pass


class CreateJournal_Request(univ.Sequence):
    pass


CreateJournal_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('journalName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0)))  
)


class DefineNamedType_Request(univ.Sequence):
    pass


DefineNamedType_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('typeName', ObjectName()),
    namedtype.NamedType('typeSpecification', TypeSpecification())
)


class InitiateUploadSequence_Request(Identifier):
    pass


class GetDomainAttributes_Request(Identifier):
    pass


class TriggerEvent_Request(univ.Sequence):
    pass


TriggerEvent_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventConditionName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('priority', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))    
)


class DefineNamedVariableList_Request(univ.Sequence):
    pass


DefineNamedVariableList_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('variableListName', ObjectName()),
    namedtype.NamedType('listOfVariable', univ.SequenceOf(componentType=univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('variableSpecification', VariableSpecification()),
        namedtype.OptionalNamedType('alternateAccess', AlternateAccess().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5)))
    ))
    ).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
)


class DeleteDomain_Request(Identifier):
    pass


class Unsigned16(univ.Integer):
    pass


class DefineSemaphore_Request(univ.Sequence):
    pass


DefineSemaphore_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('semaphoreName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('numbersOfTokens', Unsigned16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))   
)


class DeleteSemaphore_Request(ObjectName):
    pass


class TakeControl_Request(univ.Sequence):
    pass


TakeControl_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('semaphoreName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.OptionalNamedType('namedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.DefaultedNamedType('priority', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=64)),
    namedtype.OptionalNamedType('acceptableDelay', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.OptionalNamedType('controlTimeOut', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
4))),
    namedtype.OptionalNamedType('abortOnTimeOut', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
    namedtype.DefaultedNamedType('relinquishIfConnectionLost', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6)).subtype(value=1)),
    namedtype.OptionalNamedType('applicationToPreempt', ApplicationReference().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 7)))
)


class Kill_Request(univ.Sequence):
    pass


Kill_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('programInvocationName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
)


class DeleteEventAction_Request(univ.Choice):
    pass


DeleteEventAction_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('specific', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('aa-specific', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),       
    namedtype.NamedType('domain', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('vmd', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))
)


class DeleteVariableAccess_Request(univ.Sequence):
    pass


DeleteVariableAccess_Request.componentType = namedtype.NamedTypes(
#     namedtype.DefaultedNamedType('scopeOfDelete', univ.Integer(namedValues=namedval.NamedValues(('specific', 0), ('aa-specific', 1), 
# ('domain', 2), ('vmd', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=specific)),      
    namedtype.OptionalNamedType('listOfName', univ.SequenceOf(componentType=ObjectName()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('domainName', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))


class GetVariableAccessAttributes_Request(univ.Choice):
    pass


GetVariableAccessAttributes_Request.componentType = namedtype.NamedTypes(
    namedtype.NamedType('name', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),        
    namedtype.NamedType('address', Address().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class ConfirmedServiceRequest(univ.Choice):
    pass


ConfirmedServiceRequest.componentType = namedtype.NamedTypes(
    namedtype.NamedType('status', Status_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.NamedType('getNameList', GetNameList_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('identify', Identify_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),   
    namedtype.NamedType('rename', Rename_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),  
    namedtype.NamedType('read', Read_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))),      
    namedtype.NamedType('write', Write_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5))),    
    namedtype.NamedType('getVariableAccessAttributes', GetVariableAccessAttributes_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6))),
    namedtype.NamedType('defineNamedVariable', DefineNamedVariable_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 7))),
    namedtype.NamedType('defineScatteredAccess', DefineScatteredAccess_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 8))),
    namedtype.NamedType('getScatteredAccessAttributes', GetScatteredAccessAttributes_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 9))),
    namedtype.NamedType('deleteVariableAccess', DeleteVariableAccess_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 10))),
    namedtype.NamedType('defineNamedVariableList', DefineNamedVariableList_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 11))),
    namedtype.NamedType('getNamedVariableListAttributes', GetNamedVariableListAttributes_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 12))),
    namedtype.NamedType('deleteNamedVariableList', DeleteNamedVariableList_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 13))),
    namedtype.NamedType('defineNamedType', DefineNamedType_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 14))),
    namedtype.NamedType('getNamedTypeAttributes', GetNamedTypeAttributes_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 15))),
    namedtype.NamedType('deleteNamedType', DeleteNamedType_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 16))),
    namedtype.NamedType('input', Input_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 17))),   
    namedtype.NamedType('output', Output_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 18))), 
    namedtype.NamedType('takeControl', TakeControl_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 19))),
    namedtype.NamedType('relinquishControl', RelinquishControl_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 20))),
    namedtype.NamedType('defineSemaphore', DefineSemaphore_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 21))),
    namedtype.NamedType('deleteSemaphore', DeleteSemaphore_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 22))),
    namedtype.NamedType('reportSemaphoreStatus', ReportSemaphoreStatus_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 23))),
    namedtype.NamedType('reportPoolSemaphoreStatus', ReportPoolSemaphoreStatus_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 24))),
    namedtype.NamedType('reportSemaphoreEntryStatus', ReportSemaphoreEntryStatus_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 25))),
    namedtype.NamedType('initiateDownloadSequence', InitiateDownloadSequence_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 26))),
    namedtype.NamedType('downloadSegment', DownloadSegment_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 27))),
    namedtype.NamedType('terminateDownloadSequence', TerminateDownloadSequence_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 28))),
    namedtype.NamedType('initiateUploadSequence', InitiateUploadSequence_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 29))),
    namedtype.NamedType('uploadSegment', UploadSegment_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 30))),
    namedtype.NamedType('terminateUploadSequence', TerminateUploadSequence_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 31))),
    namedtype.NamedType('requestDomainDownload', RequestDomainDownload_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 32))),
    namedtype.NamedType('requestDomainUpload', RequestDomainUpload_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 33))),
    namedtype.NamedType('loadDomainContent', LoadDomainContent_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 34))),
    namedtype.NamedType('storeDomainContent', StoreDomainContent_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 35))),
    namedtype.NamedType('deleteDomain', DeleteDomain_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 36))),
    namedtype.NamedType('getDomainAttributes', GetDomainAttributes_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 37))),
    namedtype.NamedType('createProgramInvocation', CreateProgramInvocation_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 38))),
    namedtype.NamedType('deleteProgramInvocation', DeleteProgramInvocation_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 39))),
    namedtype.NamedType('start', Start_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 40))),   
    namedtype.NamedType('stop', Stop_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 41))),     
    namedtype.NamedType('resume', Resume_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 42))), 
    namedtype.NamedType('reset', Reset_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 43))),   
    namedtype.NamedType('kill', Kill_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 44))),     
    namedtype.NamedType('getProgramInvocationAttributes', GetProgramInvocationAttributes_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 45))),
    namedtype.NamedType('obtainFile', ObtainFile_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 46))),
    namedtype.NamedType('defineEventCondition', DefineEventCondition_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 47))),
    namedtype.NamedType('deleteEventCondition', DeleteEventCondition_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 48))),
    namedtype.NamedType('getEventConditionAttributes', GetEventConditionAttributes_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 49))),
    namedtype.NamedType('reportEventConditionStatus', ReportEventConditionStatus_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 50))),
    namedtype.NamedType('alterEventConditionMonitoring', AlterEventConditionMonitoring_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 51))),
    namedtype.NamedType('triggerEvent', TriggerEvent_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 52))),
    namedtype.NamedType('defineEventAction', DefineEventAction_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 53))),
    namedtype.NamedType('deleteEventAction', DeleteEventAction_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 54))),
    namedtype.NamedType('getEventActionAttributes', GetEventActionAttributes_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 55))),
    namedtype.NamedType('reportEventActionStatus', ReportEventActionStatus_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 56))),
    namedtype.NamedType('defineEventEnrollment', DefineEventEnrollment_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 57))),
    namedtype.NamedType('deleteEventEnrollment', DeleteEventEnrollment_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 58))),
    namedtype.NamedType('alterEventEnrollment', AlterEventEnrollment_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 59))),
    namedtype.NamedType('reportEventEnrollmentStatus', ReportEventEnrollmentStatus_Request().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 60))),
    namedtype.NamedType('getEventEnrollmentAttributes', GetEventEnrollmentAttributes_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 61))),
    namedtype.NamedType('acknowledgeEventNotification', AcknowledgeEventNotification_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 62))),
    namedtype.NamedType('getAlarmSummary', GetAlarmSummary_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 63))),
    namedtype.NamedType('getAlarmEnrollmentSummary', GetAlarmEnrollmentSummary_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 64))),
    namedtype.NamedType('readJournal', ReadJournal_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 65))),
    namedtype.NamedType('writeJournal', WriteJournal_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 66))),
    namedtype.NamedType('initializeJournal', InitializeJournal_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 67))),
    namedtype.NamedType('reportJournalStatus', ReportJournalStatus_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 68))),
    namedtype.NamedType('createJournal', CreateJournal_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 69))),
    namedtype.NamedType('deleteJournal', DeleteJournal_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 70))),
    namedtype.NamedType('getCapabilityList', GetCapabilityList_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 71))),
    namedtype.NamedType('fileOpen', FileOpen_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 72))),
    namedtype.NamedType('fileRead', FileRead_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 73))),  
    namedtype.NamedType('fileClose', FileClose_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 74))),    namedtype.NamedType('fileRename', FileRename_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 75))),
    namedtype.NamedType('fileDelete', FileDelete_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 76))),
    namedtype.NamedType('fileDirectory', FileDirectory_Request().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 77)))
)


class Confirmed_RequestPDU(univ.Sequence):
    pass


Confirmed_RequestPDU.componentType = namedtype.NamedTypes(
    namedtype.NamedType('invokeID', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))) #,
    # namedtype.OptionalNamedType('listOfModifier', univ.SequenceOf(componentType=Modifier())),
    # namedtype.NamedType('confirmedServiceRequest', ConfirmedServiceRequest().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))   # ,
    # namedtype.OptionalNamedType('cs-request-detail', CS_Request_Detail().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 79)))
)


class ReportPoolSemaphoreStatus_Response(univ.Sequence):
    pass


ReportPoolSemaphoreStatus_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfNamedTokens', univ.SequenceOf(componentType=univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('freeNamedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        namedtype.NamedType('ownedNamedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('hungNamedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))    ))
    ).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class EE_Class(univ.Integer):
    pass


EE_Class.namedValues = namedval.NamedValues(
    ('modifier', 0),
    ('notification', 1)
)


class EE_Duration(univ.Integer):
    pass


EE_Duration.namedValues = namedval.NamedValues(
    ('current', 0),
    ('permanent', 1)
)


class EventEnrollment(univ.Sequence):
    pass


EventEnrollment.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('eventConditionName', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('eventCondition', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType('undefined', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))      
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.OptionalNamedType('eventActionName', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('eventAction', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType('undefined', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))      
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.OptionalNamedType('clientApplication', ApplicationReference().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
    namedtype.DefaultedNamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)).subtype(value=0)),
    namedtype.NamedType('enrollmentClass', EE_Class().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),    
    # namedtype.DefaultedNamedType('duration', EE_Duration().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6)).subtype(value=current)),
    namedtype.NamedType('invokeID', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
    namedtype.OptionalNamedType('remainingAcceptableDelay', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8)))
)


class GetEventEnrollmentAttributes_Response(univ.Sequence):
    pass


GetEventEnrollmentAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfEventEnrollment', univ.SequenceOf(componentType=EventEnrollment()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=0))
)


class Reset_Response(univ.Null):
    pass


class DefineNamedVariableList_Response(univ.Null):
    pass


class DeleteVariableAccess_Response(univ.Sequence):
    pass


DeleteVariableAccess_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('numberMatched', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
    namedtype.NamedType('numberDeleted', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))     
)


class GetEventConditionAttributes_Response(univ.Sequence):
    pass


GetEventConditionAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.DefaultedNamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)),
    namedtype.NamedType('class', EC_Class().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.DefaultedNamedType('prio-rity', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)).subtype(value=64)),
    namedtype.DefaultedNamedType('severity', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)).subtype(value=64)),
    namedtype.DefaultedNamedType('alarmSummaryReports', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)).subtype(value=0)),
    namedtype.OptionalNamedType('monitoredVariable', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('variableReference', VariableSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType('undefined', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))      
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6))),
    namedtype.OptionalNamedType('evaluationInterval', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7)))
)


class ReportEventActionStatus_Response(Unsigned32):
    pass


class Input_Response(char.VisibleString):
    pass


class Stop_Response(univ.Null):
    pass


class DeleteNamedType_Response(univ.Sequence):
    pass


DeleteNamedType_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('numberMatched', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
    namedtype.NamedType('numberDeleted', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))     
)


class UploadSegment_Response(univ.Sequence):
    pass


UploadSegment_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('loadData', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('non-coded', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        # namedtype.NamedType('coded', EXTERNALt())
    ))
    ),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class FileAttributes(univ.Sequence):
    pass


FileAttributes.componentType = namedtype.NamedTypes(
    namedtype.NamedType('sizeOfFile', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.OptionalNamedType('lastModified', useful.GeneralizedTime().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class FileOpen_Response(univ.Sequence):
    pass


FileOpen_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('frsmID', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('fileAttributes', FileAttributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class DeleteJournal_Response(univ.Null):
    pass


class DefineEventCondition_Response(univ.Null):
    pass


class Identify_Response(univ.Sequence):
    pass


Identify_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('vendorName', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('modelName', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),    namedtype.NamedType('revision', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), 
    namedtype.OptionalNamedType('listOfAbstractSyntaxes', univ.SequenceOf(componentType=univ.ObjectIdentifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3)))
)


class Kill_Response(univ.Null):
    pass


class GetNameList_Response(univ.Sequence):
    pass


GetNameList_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfIdentifier', univ.SequenceOf(componentType=Identifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class Resume_Response(univ.Null):
    pass


class Output_Response(univ.Null):
    pass


class DefineEventAction_Response(univ.Null):
    pass


class InitiateDownloadSequence_Response(univ.Null):
    pass


class LoadDomainContent_Response(univ.Null):
    pass


class StoreDomainContent_Response(univ.Null):
    pass


class TakeControl_Response(univ.Choice):
    pass


TakeControl_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('noResult', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('namedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))        
)


class GetEventActionAttributes_Response(univ.Sequence):
    pass


GetEventActionAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.DefaultedNamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)),
    namedtype.NamedType('listOfModifier', univ.SequenceOf(componentType=Modifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, 
tag.tagFormatSimple, 1)))
)


class WriteJournal_Response(univ.Null):
    pass


class DeleteEventCondition_Response(Unsigned32):
    pass


class DirectoryEntry(univ.Sequence):
    pass


DirectoryEntry.componentType = namedtype.NamedTypes(
    namedtype.NamedType('filename', FileName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('fileAttributes', FileAttributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)))
)


class FileDirectory_Response(univ.Sequence):
    pass


FileDirectory_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfDirectoryEntry', univ.SequenceOf(componentType=DirectoryEntry()).subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=0))
)


class ObtainFile_Response(univ.Null):
    pass


class GetNamedTypeAttributes_Response(univ.Sequence):
    pass


GetNamedTypeAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.NamedType('typeSpecification', TypeSpecification())
)


class GetProgramInvocationAttributes_Response(univ.Sequence):
    pass


GetProgramInvocationAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('state', ProgramInvocationState().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    namedtype.NamedType('listOfDomainNames', univ.SequenceOf(componentType=Identifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),   
    namedtype.NamedType('reusable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),       
    namedtype.NamedType('monitor', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),        
    namedtype.NamedType('startArgument', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
    namedtype.OptionalNamedType('executionArgument', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('simpleString', char.VisibleString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        # namedtype.NamedType('encodedString', EXTERNALt())
    ))
    )
)


class DeleteEventAction_Response(Unsigned32):
    pass


class GetScatteredAccessAttributes_Response(univ.Sequence):
    pass


GetScatteredAccessAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.NamedType('scatteredAccessDescription', ScatteredAccessDescription().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class ReportEventEnrollmentStatus_Response(univ.Sequence):
    pass


ReportEventEnrollmentStatus_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventConditionTransitions', Transitions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('notificationLost', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value=0)),
    namedtype.NamedType('duration', EE_Duration().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),        
    namedtype.OptionalNamedType('alarmAcknowledgmentRule', AlarmAckRule().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('currentState', EE_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)))        
)


class ReportEventConditionStatus_Response(univ.Sequence):
    pass


ReportEventConditionStatus_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('currentState', EC_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),       
    namedtype.NamedType('numberOfEventEnrollments', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.OptionalNamedType('enabled', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),    namedtype.OptionalNamedType('timeOfLastTransitionToActive', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
    namedtype.OptionalNamedType('timeOfLastTransitionToIdle', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4)))
)


class RelinquishControl_Response(univ.Null):
    pass


class CreateJournal_Response(univ.Null):
    pass


class DeleteProgramInvocation_Response(univ.Null):
    pass


class FileClose_Response(univ.Null):
    pass


class Write_Response(univ.SequenceOf):
    pass


Write_Response.componentType = univ.Choice(componentType=namedtype.NamedTypes(
    namedtype.NamedType('failure', DataAccessError().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),     
    namedtype.NamedType('success', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
))


class DefineSemaphore_Response(univ.Null):
    pass


class TerminateDownloadSequence_Response(univ.Null):
    pass


class DefineScatteredAccess_Response(univ.Null):
    pass


class DeleteDomain_Response(univ.Null):
    pass


class DownloadSegment_Response(univ.Sequence):
    pass


DownloadSegment_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('loadData', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('non-coded', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
        # namedtype.NamedType('coded', EXTERNALt())
    ))
    ),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class DefineNamedType_Response(univ.Null):
    pass


class Integer8(univ.Integer):
    pass


class DomainState(univ.Integer):
    pass


DomainState.namedValues = namedval.NamedValues(
    ('non-existent', 0),
    ('loading', 1),
    ('ready', 2),
    ('in-use', 3),
    ('complete', 4),
    ('incomplete', 5),
    ('d1', 7),
    ('d2', 8),
    ('d3', 9),
    ('d4', 10),
    ('d5', 11),
    ('d6', 12),
    ('d7', 13),
    ('d8', 14),
    ('d9', 15)
)


class GetDomainAttributes_Response(univ.Sequence):
    pass


GetDomainAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfCapabilities', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('state', DomainState().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),   
    namedtype.NamedType('sharable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),       
    namedtype.NamedType('listOfProgramInvocations', univ.SequenceOf(componentType=Identifier()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
    namedtype.NamedType('uploadInProgress', Integer8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5)))    
)


class GetAlarmEnrollmentSummary_Response(univ.Sequence):
    pass


GetAlarmEnrollmentSummary_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfAlarmEnrollmentSummary', univ.SequenceOf(componentType=AlarmEnrollmentSummary()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=0))
)


class Rename_Response(univ.Null):
    pass


class FileRead_Response(univ.Sequence):
    pass


FileRead_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('fileData', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class GetAlarmSummary_Response(univ.Sequence):
    pass


GetAlarmSummary_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfAlarmSummary', univ.SequenceOf(componentType=AlarmSummary()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=0))
)


class DefineNamedVariable_Response(univ.Null):
    pass


class InitiateUploadSequence_Response(univ.Sequence):
    pass


InitiateUploadSequence_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('ulsmID', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('listOfCapabilities', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class JournalEntry(univ.Sequence):
    pass


JournalEntry.componentType = namedtype.NamedTypes(
    namedtype.NamedType('entryIdentifier', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('originatingApplication', ApplicationReference().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('entryContent', EntryContent().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class ReadJournal_Response(univ.Sequence):
    pass


ReadJournal_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfJournalEntry', univ.SequenceOf(componentType=JournalEntry()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=0))
)


class RequestDomainUpload_Response(univ.Null):
    pass


class FileRename_Response(univ.Null):
    pass


class TriggerEvent_Response(univ.Null):
    pass


class CreateProgramInvocation_Response(univ.Null):
    pass


class FileDelete_Response(univ.Null):
    pass


class Status_Response(univ.Sequence):
    pass


Status_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('vmdLogicalStatus', univ.Integer(namedValues=namedval.NamedValues(('state-changes-allowed', 0), ('no-state-changes-allowed', 1), ('limited-services-allowed', 2), ('support-services-allowed', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('vmdPhysicalStatus', univ.Integer(namedValues=namedval.NamedValues(('operational', 0), ('partially-operational', 1), ('inoperable', 2), ('needs-commissioning', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),  
    namedtype.OptionalNamedType('localDetail', univ.BitString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 128)).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class InitializeJournal_Response(Unsigned32):
    pass


class TerminateUploadSequence_Response(univ.Null):
    pass


class DeleteSemaphore_Response(univ.Null):
    pass


class Read_Response(univ.Sequence):
    pass


Read_Response.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('variableAccessSpecificatn', VariableAccessSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('listOfAccessResult', univ.SequenceOf(componentType=AccessResult()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class DefineEventEnrollment_Response(univ.Null):
    pass


class GetNamedVariableListAttributes_Response(univ.Sequence):
    pass


GetNamedVariableListAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.NamedType('listOfVariable', univ.SequenceOf(componentType=univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('variableSpecification', VariableSpecification()),
        namedtype.OptionalNamedType('alternateAccess', AlternateAccess().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5)))
    ))
    ).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class DeleteEventEnrollment_Response(Unsigned32):
    pass


class GetVariableAccessAttributes_Response(univ.Sequence):
    pass


GetVariableAccessAttributes_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.OptionalNamedType('address', Address().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),    namedtype.NamedType('typeSpecification', TypeSpecification().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class RequestDomainDownload_Response(univ.Null):
    pass


class DeleteNamedVariableList_Response(univ.Sequence):
    pass


DeleteNamedVariableList_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('numberMatched', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
    namedtype.NamedType('numberDeleted', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))     
)


class Start_Response(univ.Null):
    pass


class SemaphoreEntry(univ.Sequence):
    pass


SemaphoreEntry.componentType = namedtype.NamedTypes(
    namedtype.NamedType('entryId', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),    
    namedtype.NamedType('entryClass', univ.Integer(namedValues=namedval.NamedValues(('simple', 0), ('modifier', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('applicationReference', ApplicationReference().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.OptionalNamedType('namedToken', Identifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.DefaultedNamedType('priority', Priority().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4)).subtype(value=64)),
    namedtype.OptionalNamedType('remainingTimeOut', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
    namedtype.OptionalNamedType('abortOnTimeOut', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
    namedtype.DefaultedNamedType('relinquishIfConnectionLost', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7)).subtype(value=1))
)


class ReportSemaphoreEntryStatus_Response(univ.Sequence):
    pass


ReportSemaphoreEntryStatus_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfSemaphoreEntry', univ.SequenceOf(componentType=SemaphoreEntry()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class ReportSemaphoreStatus_Response(univ.Sequence):
    pass


ReportSemaphoreStatus_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.NamedType('class', univ.Integer(namedValues=namedval.NamedValues(('token', 0), ('pool', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('numberOfTokens', Unsigned16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),   
    namedtype.NamedType('numberOfOwnedTokens', Unsigned16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('numberOfHungTokens', Unsigned16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))))


class ReportJournalStatus_Response(univ.Sequence):
    pass


ReportJournalStatus_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('currentEntries', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),   
    namedtype.NamedType('mmsDeletable', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))    
)


class GetCapabilityList_Response(univ.Sequence):
    pass


GetCapabilityList_Response.componentType = namedtype.NamedTypes(
    namedtype.NamedType('listOfCapabilities', univ.SequenceOf(componentType=char.VisibleString()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.DefaultedNamedType('moreFollows', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
1)).subtype(value=1))
)


class ConfirmedServiceResponse(univ.Choice):
    pass


ConfirmedServiceResponse.componentType = namedtype.NamedTypes(
    namedtype.NamedType('status', Status_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), 
    namedtype.NamedType('getNameList', GetNameList_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('identify', Identify_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.NamedType('rename', Rename_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),      
    namedtype.NamedType('read', Read_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))),     
    namedtype.NamedType('write', Write_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),        
    namedtype.NamedType('getVariableAccessAttributes', GetVariableAccessAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 6))),
    namedtype.NamedType('defineNamedVariable', DefineNamedVariable_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
    namedtype.NamedType('defineScatteredAccess', DefineScatteredAccess_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))),
    namedtype.NamedType('getScatteredAccessAttributes', GetScatteredAccessAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 9))),
    namedtype.NamedType('deleteVariableAccess', DeleteVariableAccess_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 10))),
    namedtype.NamedType('defineNamedVariableList', DefineNamedVariableList_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 11))),
    namedtype.NamedType('getNamedVariableListAttributes', GetNamedVariableListAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 12))),
    namedtype.NamedType('deleteNamedVariableList', DeleteNamedVariableList_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 13))),
    namedtype.NamedType('defineNamedType', DefineNamedType_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 14))),
    namedtype.NamedType('getNamedTypeAttributes', GetNamedTypeAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 15))),
    namedtype.NamedType('deleteNamedType', DeleteNamedType_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 16))),
    namedtype.NamedType('input', Input_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 17))),       
    namedtype.NamedType('output', Output_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 18))),     
    namedtype.NamedType('takeControl', TakeControl_Response().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 19))),
    namedtype.NamedType('relinquishControl', RelinquishControl_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 20))),
    namedtype.NamedType('defineSemaphore', DefineSemaphore_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 21))),
    namedtype.NamedType('deleteSemaphore', DeleteSemaphore_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 22))),
    namedtype.NamedType('reportSemaphoreStatus', ReportSemaphoreStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 23))),
    namedtype.NamedType('reportPoolSemaphoreStatus', ReportPoolSemaphoreStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 24))),
    namedtype.NamedType('reportSemaphoreEntryStatus', ReportSemaphoreEntryStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 25))),
    namedtype.NamedType('initiateDownloadSequence', InitiateDownloadSequence_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 26))),
    namedtype.NamedType('downloadSegment', DownloadSegment_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 27))),
    namedtype.NamedType('terminateDownloadSequence', TerminateDownloadSequence_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 28))),
    namedtype.NamedType('initiateUploadSequence', InitiateUploadSequence_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 29))),
    namedtype.NamedType('uploadSegment', UploadSegment_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 30))),
    namedtype.NamedType('terminateUploadSequence', TerminateUploadSequence_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 31))),
    namedtype.NamedType('requestDomainDownLoad', RequestDomainDownload_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 32))),
    namedtype.NamedType('requestDomainUpload', RequestDomainUpload_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 33))),
    namedtype.NamedType('loadDomainContent', LoadDomainContent_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 34))),
    namedtype.NamedType('storeDomainContent', StoreDomainContent_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 35))),
    namedtype.NamedType('deleteDomain', DeleteDomain_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 36))),
    namedtype.NamedType('getDomainAttributes', GetDomainAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 37))),
    namedtype.NamedType('createProgramInvocation', CreateProgramInvocation_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 38))),
    namedtype.NamedType('deleteProgramInvocation', DeleteProgramInvocation_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 39))),
    namedtype.NamedType('start', Start_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 40))),       
    namedtype.NamedType('stop', Stop_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 41))),
    namedtype.NamedType('resume', Resume_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 42))),     
    namedtype.NamedType('reset', Reset_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 43))),       
    namedtype.NamedType('kill', Kill_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 44))),
    namedtype.NamedType('getProgramInvocationAttributes', GetProgramInvocationAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 45))),
    namedtype.NamedType('obtainFile', ObtainFile_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 46))),
    namedtype.NamedType('fileOpen', FileOpen_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 72))),
    namedtype.NamedType('defineEventCondition', DefineEventCondition_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 47))),
    namedtype.NamedType('deleteEventCondition', DeleteEventCondition_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 48))),
    namedtype.NamedType('getEventConditionAttributes', GetEventConditionAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 49))),
    namedtype.NamedType('reportEventConditionStatus', ReportEventConditionStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 50))),
    namedtype.NamedType('alterEventConditionMonitoring', AlterEventConditionMonitoring_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 51))),
    namedtype.NamedType('triggerEvent', TriggerEvent_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 52))),
    namedtype.NamedType('defineEventAction', DefineEventAction_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 53))),
    namedtype.NamedType('deleteEventAction', DeleteEventAction_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 54))),
    namedtype.NamedType('getEventActionAttributes', GetEventActionAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 55))),
    namedtype.NamedType('reportActionStatus', ReportEventActionStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 56))),
    namedtype.NamedType('defineEventEnrollment', DefineEventEnrollment_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 57))),
    namedtype.NamedType('deleteEventEnrollment', DeleteEventEnrollment_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 58))),
    namedtype.NamedType('alterEventEnrollment', AlterEventEnrollment_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 59))),
    namedtype.NamedType('reportEventEnrollmentStatus', ReportEventEnrollmentStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 60))),
    namedtype.NamedType('getEventEnrollmentAttributes', GetEventEnrollmentAttributes_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 61))),
    namedtype.NamedType('acknowledgeEventNotification', AcknowledgeEventNotification_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 62))),
    namedtype.NamedType('getAlarmSummary', GetAlarmSummary_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 63))),
    namedtype.NamedType('getAlarmEnrollmentSummary', GetAlarmEnrollmentSummary_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 64))),
    namedtype.NamedType('readJournal', ReadJournal_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 65))),
    namedtype.NamedType('writeJournal', WriteJournal_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 66))),
    namedtype.NamedType('initializeJournal', InitializeJournal_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 67))),
    namedtype.NamedType('reportJournalStatus', ReportJournalStatus_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 68))),
    namedtype.NamedType('createJournal', CreateJournal_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 69))),
    namedtype.NamedType('deleteJournal', DeleteJournal_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 70))),
    namedtype.NamedType('getCapabilityList', GetCapabilityList_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 71))),
    namedtype.NamedType('fileRead', FileRead_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 73))),
    namedtype.NamedType('fileClose', FileClose_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 74))),
    namedtype.NamedType('fileRename', FileRename_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 75))),
    namedtype.NamedType('fileDelete', FileDelete_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 76))),
    namedtype.NamedType('fileDirectory', FileDirectory_Response().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 77)))
)


class Confirmed_ResponsePDU(univ.Sequence):
    pass


Confirmed_ResponsePDU.componentType = namedtype.NamedTypes(
    namedtype.NamedType('invokeID', Unsigned32()),
    namedtype.NamedType('confirmedServiceResponse', ConfirmedServiceResponse())  #,
    # namedtype.OptionalNamedType('cs-request-detail', CS_Request_Detail().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 79)))
)


class EventNotification(univ.Sequence):
    pass


EventNotification.componentType = namedtype.NamedTypes(
    namedtype.NamedType('eventEnrollmentName', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('eventConditionName', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('eventCondition', ObjectName().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
        namedtype.NamedType('undefined', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))      
    ))
    .subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('severity', Unsigned8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('currentState', EC_State().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('transitionTime', EventTime().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))),
    namedtype.DefaultedNamedType('notificationLost', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6)).subtype(value=0)),
    namedtype.OptionalNamedType('alarmAcknowledgmentRule', AlarmAckRule().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
    namedtype.OptionalNamedType('actionResult', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('eventActioName', ObjectName()),
        namedtype.NamedType('eventActionResult', univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('success', ConfirmedServiceResponse().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
            namedtype.NamedType('failure', ServiceError().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 
1)))
        ))
        )
    ))
    .subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 8)))
)


class InformationReport(univ.Sequence):
    pass


InformationReport.componentType = namedtype.NamedTypes(
    namedtype.NamedType('variableAccessSpecification', VariableAccessSpecification()),
    namedtype.NamedType('listOfAccessResult', univ.SequenceOf(componentType=AccessResult()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
)


class Integer16(univ.Integer):
    pass


class ParameterSupportOptions(univ.BitString):
    pass


ParameterSupportOptions.namedValues = namedval.NamedValues(
    ('str1', 0),
    ('str2', 1),
    ('vnam', 2),
    ('valt', 3),
    ('vadr', 4),
    ('vsca', 5),
    ('tpy', 6),
    ('vlis', 7),
    ('real', 8),
    ('cei', 10)
)


class ServiceSupportOptions(univ.BitString):
    pass


ServiceSupportOptions.namedValues = namedval.NamedValues(
    ('status', 0),
    ('getNameList', 1),
    ('identify', 2),
    ('rename', 3),
    ('read', 4),
    ('write', 5),
    ('getVariableAccessAttributes', 6),
    ('defineNamedVariable', 7),
    ('defineScatteredAccess', 8),
    ('getScatteredAccessAttributes', 9),
    ('deleteVariableAccess', 10),
    ('defineNamedVariableList', 11),
    ('getNamedVariableListAttributes', 12),
    ('deleteNamedVariableList', 13),
    ('defineNamedType', 14),
    ('getNamedTypeAttributes', 15),
    ('deleteNamedType', 16),
    ('input', 17),
    ('output', 18),
    ('takeControl', 19),
    ('relinquishControl', 20),
    ('defineSemaphore', 21),
    ('deleteSemaphore', 22),
    ('reportSemaphoreStatus', 23),
    ('reportPoolSemaphoreStatus', 24),
    ('reportSemaphoreEntryStatus', 25),
    ('initiateDownloadSequence', 26),
    ('downloadSegment', 27),
    ('terminateDownloadSequence', 28),
    ('initiateUploadSequence', 29),
    ('uploadSegment', 30),
    ('terminateUploadSequence', 31),
    ('requestDomainDownload', 32),
    ('requestDomainUpload', 33),
    ('loadDomainContent', 34),
    ('storeDomainContent', 35),
    ('deleteDomain', 36),
    ('getDomainAttributes', 37),
    ('createProgramInvocation', 38),
    ('deleteProgramInvocation', 39),
    ('start', 40),
    ('stop', 41),
    ('resume', 42),
    ('reset', 43),
    ('kill', 44),
    ('getProgramInvocationAttributes', 45),
    ('obtainFile', 46),
    ('defineEventCondition', 47),
    ('deleteEventCondition', 48),
    ('getEventConditionAttributes', 49),
    ('reportEventConditionStatus', 50),
    ('alterEventConditionMonitoring', 51),
    ('triggerEvent', 52),
    ('defineEventAction', 53),
    ('deleteEventAction', 54),
    ('getEventActionAttributes', 55),
    ('reportActionStatus', 56),
    ('defineEventEnrollment', 57),
    ('deleteEventEnrollment', 58),
    ('alterEventEnrollment', 59),
    ('reportEventEnrollmentStatus', 60),
    ('getEventEnrollmentAttributes', 61),
    ('acknowledgeEventNotification', 62),
    ('getAlarmSummary', 63),
    ('getAlarmEnrollmentSummary', 64),
    ('readJournal', 65),
    ('writeJournal', 66),
    ('initializeJournal', 67),
    ('reportJournalStatus', 68),
    ('createJournal', 69),
    ('deleteJournal', 70),
    ('getCapabilityList', 71),
    ('fileOpen', 72),
    ('fileRead', 73),
    ('fileClose', 74),
    ('fileRename', 75),
    ('fileDelete', 76),
    ('fileDirectory', 77),
    ('unsolicitedStatus', 78),
    ('informationReport', 79),
    ('eventNotification', 80),
    ('attachToEventCondition', 81),
    ('attachToSemaphore', 82),
    ('conclude', 83),
    ('cancel', 84)
)


class InitRequestDetail(univ.Sequence):
    pass


InitRequestDetail.componentType = namedtype.NamedTypes(
    namedtype.NamedType('proposedVersionNumber', Integer16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('proposedParameterCBB', ParameterSupportOptions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('servicesSupportedCalling', ServiceSupportOptions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class InitResponseDetail(univ.Sequence):
    pass


InitResponseDetail.componentType = namedtype.NamedTypes(
    namedtype.NamedType('negociatedVersionNumber', Integer16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 
0))),
    namedtype.NamedType('negociatedParameterCBB', ParameterSupportOptions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('servicesSupportedCalled', ServiceSupportOptions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)))
)


class Initiate_ErrorPDU(ServiceError):
    pass


class Initiate_RequestPDU(univ.Sequence):
    pass


Initiate_RequestPDU.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('localDetailCalling', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('proposedMaxServOutstandingCalling', Integer16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('proposedMaxServOutstandingCalled', Integer16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('proposedDataStructureNestingLevel', Integer8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('mmsInitRequestDetail', InitRequestDetail().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4)))
)


class Initiate_ResponsePDU(univ.Sequence):
    pass


Initiate_ResponsePDU.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('localDetailCalled', Integer32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('negociatedMaxServOutstandingCalling', Integer16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
    namedtype.NamedType('negociatedMaxServOutstandingCalled', Integer16().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
    namedtype.OptionalNamedType('negociatedDataStructureNestingLevel', Integer8().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
    namedtype.NamedType('mmsInitResponseDetail', InitResponseDetail().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4)))
)


class RejectPDU(univ.Sequence):
    pass


RejectPDU.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('originalInvokeID', Unsigned32().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.NamedType('rejectReason', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('confirmed-requestPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('unrecognized-service', 1), ('unrecognized-modifier', 2), ('invalid-invokeID', 3), ('invalid-argument', 4), ('invalid-modifier', 5), ('max-serv-outstanding-exceeded', 6), ('max-recursion-exceeded', 8), ('value-out-of-range', 9))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
        namedtype.NamedType('confirmed-responsePDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('unrecognized-service', 1), ('invalid-invokeID', 2), ('invalid-result', 3), ('max-recursion-exceeded', 5), ('value-out-of-range', 6))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
        namedtype.NamedType('confirmed-errorPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('unrecognized-service', 1), ('invalid-invokeID', 2), ('invalid-serviceError', 3), ('value-out-of-range', 4))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))),
        namedtype.NamedType('unconfirmedPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('unrecognized-service', 1), ('invalid-argument', 2), ('max-recursion-exceeded', 3), ('value-out-of-range', 4))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
        namedtype.NamedType('pdu-error', univ.Integer(namedValues=namedval.NamedValues(('unknown-pdu-type', 0), ('invalid-pdu', 1), ('illegal-acse-mapping', 2))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
        namedtype.NamedType('cancel-requestPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invalid-invokeID', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
        namedtype.NamedType('cancel-responsePDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invalid-invokeID', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
        namedtype.NamedType('cancel-errorPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invalid-invokeID', 1), ('invalid-serviceError', 2), ('value-out-of-range', 3))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))),  
        namedtype.NamedType('conclude-requestPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invalid-argument', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 9))),
        namedtype.NamedType('conclude-responsePDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invalid-result', 1))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 10))),
        namedtype.NamedType('conclude-errorPDU', univ.Integer(namedValues=namedval.NamedValues(('other', 0), ('invalid-serviceError', 1), ('value-out-of-range', 2))).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 11)))
    ))
    )
)


class UnsolicitedStatus(Status_Response):
    pass


class UnconfirmedService(univ.Choice):
    pass


UnconfirmedService.componentType = namedtype.NamedTypes(
    namedtype.NamedType('informationReport', InformationReport().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('unsolicitedStatus', UnsolicitedStatus().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('eventNotification', EventNotification().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2)))
)


class Unconfirmed_PDU(univ.Sequence):
    pass


Unconfirmed_PDU.componentType = namedtype.NamedTypes(
    namedtype.NamedType('unconfirmedService', UnconfirmedService()),
    namedtype.OptionalNamedType('cs-request-detail', CS_Request_Detail().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 79)))
)


class MMSpdu(univ.Choice):
    pass


MMSpdu.componentType = namedtype.NamedTypes(
    namedtype.NamedType('confirmed-RequestPDU', Confirmed_RequestPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))),
    namedtype.NamedType('confirmed-ResponsePDU', Confirmed_ResponsePDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))),
    namedtype.NamedType('confirmed-ErrorPDU', Confirmed_ErrorPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))),
    namedtype.NamedType('unconfirmed-PDU', Unconfirmed_PDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))),
    namedtype.NamedType('rejectPDU', RejectPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))),    
    namedtype.NamedType('cancel-RequestPDU', Cancel_RequestPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))),
    namedtype.NamedType('cancel-ResponsePDU', Cancel_ResponsePDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
    namedtype.NamedType('cancel-ErrorPDU', Cancel_ErrorPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 7))),
    namedtype.NamedType('initiate-RequestPDU', Initiate_RequestPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 8))),
    namedtype.NamedType('initiate-ResponsePDU', Initiate_ResponsePDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 9))),
    namedtype.NamedType('initiate-ErrorPDU', Initiate_ErrorPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 10))),
    namedtype.NamedType('conclude-RequestPDU', Conclude_RequestPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 11))),
    namedtype.NamedType('conclude-ResponsePDU', Conclude_ResponsePDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 12))),
    namedtype.NamedType('conclude-ErrorPDU', Conclude_ErrorPDU().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 13)))
)


normalPriority = Priority(64)
