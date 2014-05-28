

class SnmpError(Exception):
    """Base class for exceptions raised during snmp"""
    message = "An error occured when communicating over snmp."
    def __init__(self, errorStatus, errorIndex):
        self.errorStatus = errorStatus
        self.errorIndex = errorIndex
    
    def __str__(self):
        return self.message + (" Error Status:"
        "%s. Error Index: %s") % self.errorStatus, self.errorIndex

class SnmpActivationError(SnmpError):
    message = "An error occured turning the PDU on or off"
