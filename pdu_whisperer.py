#thanks checkaa for the name
from collections import namedtuple
from pysnmp import debug
#from pysnmp.smi import builder, view
from pysnmp.entity.rfc3413.oneliner import cmdgen

import pdu_exceptions

"""tower, infeed, and outfeed should  be small integers"""
Outlet = namedtuple('outlet', 'tower infeed outfeed', verbose=False)

class PduWhisperer(object):

    def __init__(port=161):
        self.port = port
        self.cmdGen = cmdgen.CommandGenerator()

    def scan_pdus(pdus):
        """Scans all the pdus and returns a list of named tuples"""
        for pdu in pdus:
            errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
                cmdgen.CommunityData('OSL_private'),
                cmdgen.UdpTransportTarget((pdu, self.port)),
                cmdgen.MibVariable('Sentry3',''),
                lookupNames=True, lookupValues=True, lexicographicMode=True,
                ignoreNonIncreasingOid=True
            )

        pdu_data_list = []
        # Check for errors and print out results
        if errorIndication:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            if errorStatus:
                raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        modName, symName, suffix = mibViewController.getNodeLocation((name))
                        print "%s - %s - %s - %s" % (pdu, symName, suffix, val)
                        print "-------"
                        pdu_data_list.append(pdu_data(modName, symName, suffix))
                        #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        return pdu_data_list

    def outlet_is_on(pdu, outlet):
        """Returns true if the outlet is on. If the outlet is off, rebooting,
        or in some other state it will return false"""
        if outlet_status == 1:
            return True
        else:
            return False

    def _sendGetCommand(pdu, outlet, command):
        """Private function to send a given get command name to a pdu"""
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('OSL_private'),
            cmdgen.UdpTransportTarget((pdu, self.port)),
            cmdgen.MibVariable('Sentry3', command, outlet.tower, outlet.infeed,
                outlet.outfeed)
        )
        if errorIndication:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            if errorStatus:
                raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
            else:
                return varBinds

    def outlet_status(pdu, outlet):
        """Return the outlet's status. Maybe one of:
            * 0 = none
            * 1 = on
            * 2 = off
            * 3 = reboot"""
        varBinds = _sendGetCommand(pdu, outlet, 'outletStatus')
        return [reply[1] for reply in varBinds]

    def get_outlet_state(pdu, outlet):
        varBinds = _sendGetCommand(pdu, outlet, 'outletControlState')
        return [reply[1] for reply in varBinds]


    def get_outlet_voltage(pdu, outlet):
        varBinds = _sendGetCommand(pdu, outlet, 'outletVoltage')
        return [reply[1] for reply in varBinds]


    def get_outlet_power_consumption(pdu, outlet):
        varBinds = _sendGetCommand(pdu, outlet, 'outletPower')
        return [reply[1] for reply in varBinds]

    def get_outlet_name(pdu, outlet):
        varBinds = _sendGetCommand(pdu, outlet, 'outletName')
        return [reply[1] for reply in varBinds]

    def get_pdu_group(pdu):
        pass

    def outlet_list(pdu):
        pass

    def group_outlets(outlets, groupname):
        pass

    def turn_off_outlet(pdu, outlet):
        """Turn the outlet on"""
        _turn_outlet(pdu, outlet, 'off')

    def turn_on_outlet(pdu, outlet):
        """Turn the outlet on"""
        _turn_outlet(pdu, outlet, 'on')

    def reboot_outlet(pdu, outlet):
        """Power cycle the outlet"""

        _turn_outlet(pdu, outlet, 3)

    def _turn_outlet(pdu, outlet, status):
        """Private helper function to set a pdu to a given status. Statuses
        may be one of:
             * 0 = none
            * 1 = on    
            * 2 = off     
            * 3 = reboot"""
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
            cmdgen.CommunityData('OSL_private'),
            cmdgen.UdpTransportTarget((ip_address, self.port)),
            (cmdgen.MibVariable('Sentry3', 'outletControlAction', outlet.tower,
            outlet.infeed, outlet.outfeed), status)
        )

        # Check for errors. If found, raise an exception
        if errorIndication:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

