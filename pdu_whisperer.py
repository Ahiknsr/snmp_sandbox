#thanks checkaa for the name
from collections import namedtuple
from pysnmp import debug
#from pysnmp.smi import builder, view
from pysnmp.entity.rfc3413.oneliner import cmdgen

import pdu_exceptions

"""tower, infeed, and outfeed should  be small integers"""
Outlet = namedtuple('outlet', 'tower infeed outfeed', verbose=False)

class PduWhisperer(object):

    def __init__(port=None):
        if port != None:
            self.port = port
        else:
            self.port = 161
        self.cmdGen = cmdgen.CommandGenerator()

    def scan_pdus(pdus):
        """Scans all the pdus and returns a list of named tuples"""
        for pdu in pdus:
            errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
                cmdgen.CommunityData('OSL_private'),
                cmdgen.UdpTransportTarget((pdu, port)),
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

    def get_outlet_power_state(pdu, outlet):
        pass

    def get_outlet_power_consumption(pdu, outlet):
        pass

    def get_outlets_in_same_group(pdu, outlet):
        pass

    def get_outlet_group(pdu, outlet):
        pass

    def group_list(pdu, group_name):
        pass

    def outlet_list(pdu):
        pass

    def group_outlets(outlets, groupname):
        pass

    def turn_off_outlet(pdu, outlet):
        _turn_outlet(pdu, outlet, 'off')

    def turn_on_outlet(pdu, outlet):
        _turn_outlet(pdu, outlet, 'on')

    def _turn_outlet(pdu, outlet, status):
        """
        The following sets the value of the outletcontrol action for outlet
        4 on infeed 1 on tower 2 to "on", effectively turning the outlet on
        """

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

