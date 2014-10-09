#thanks checkaa for the name
import os
from collections import namedtuple
from pysnmp import debug
from pysnmp.smi import builder, view
from pysnmp.entity.rfc3413.oneliner import cmdgen

from pdumaster import pdu_exceptions

"""tower, infeed, and outfeed should  be small integers"""
Outlet = namedtuple('outlet', ['tower', 'infeed', 'outfeed',], verbose=False)


class PduWhisperer(object):

    def __init__(self, port=161):
        self.port = port
        self.cmdgen = cmdgen.CommandGenerator()
        self.build_mibs()

    def build_mibs(self):
        mibdir = "%s/mib" % os.path.dirname(os.path.realpath(__file__))

        # create MIB builder
        #mibBuilder = builder.MibBuilder()

        mibBuilder = self.cmdgen.snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

        # load mibs
        mibSources = mibBuilder.getMibSources() + (builder.DirMibSource(mibdir),)
        mibBuilder.setMibSources(*mibSources)

        mibBuilder.loadModules('SNMPv2-MIB', 'IF-MIB', 'Sentry3')

        # the view controller is handy for viewing objects
        self.mibViewController = view.MibViewController(mibBuilder)

    def scan_pdus(self, pdus):
        """Scans all the pdus and returns a list of named tuples"""
        for pdu in pdus:
            errorIndication, errorStatus, errorIndex, varBindTable = self.cmdgen.nextCmd(
                cmdgen.CommunityData('OSL_private'),
                cmdgen.UdpTransportTarget((pdu, self.port)),
                cmdgen.MibVariable('Sentry3', ''),
                lookupNames=True, lookupValues=True, lexicographicMode=True,
                ignoreNonIncreasingOid=True
            )

        pdu_data_list = []
        # Check for errors and print out results
        if errorIndication:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            if errorStatus:
                raise pdu_exceptions.SnmpActivationError(
                    errorStatus,
                    errorIndex
                )
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        modName, symName, suffix = self.mibViewController.getNodeLocation((name))
                        print "%s - %s - %s - %s" % (pdu, symName, suffix, val)
                        print "-------"
                        pdu_data_list.append(
                                (
                                modName,
                                symName,
                                suffix
                                )
                        )
        return pdu_data_list

    def outlet_is_on(self, pdu, outlet):
        """Returns true if the outlet is on. If the outlet is off, rebooting,
        or in some other state it will return false"""
        if outlet_status == 1:
            return True
        else:
            return False

    def _sendGetCommand(self, pdu, outlet, command):
        """Private function to send a given get command name to a pdu"""
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdgen.getCmd(
            cmdgen.CommunityData('OSL_private'),
            cmdgen.UdpTransportTarget((pdu, self.port)),
            cmdgen.MibVariable(
                'Sentry3',
                command,
                outlet.tower,
                outlet.infeed,
                outlet.outfeed
            )
        )
        if errorIndication:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            if errorStatus:
                raise pdu_exceptions.SnmpActivationError(
                    errorStatus,
                    errorIndex
                )
            else:
                return varBinds

    def outlet_status(self, pdu, outlet):
        """Return the outlet's status. Maybe one of:
            * 0 = none
            * 1 = on
            * 2 = off
            * 3 = reboot"""
        varBinds = self._sendGetCommand(pdu, outlet, 'outletStatus')
        return [reply[1] for reply in varBinds]

    def get_outlet_state(self, pdu, outlet):
        varBinds = self._sendGetCommand(pdu, outlet, 'outletControlState')
        return [reply[1] for reply in varBinds]

    def get_outlet_voltage(self, pdu, outlet):
        varBinds = self._sendGetCommand(pdu, outlet, 'outletVoltage')
        return [reply[1] for reply in varBinds]

    def get_outlet_power_consumption(self, pdu, outlet):
        varBinds = self._sendGetCommand(pdu, outlet, 'outletPower')
        return [reply[1] for reply in varBinds]

    def get_outlet_name(self, pdu, outlet):
        varBinds = self._sendGetCommand(pdu, outlet, 'outletName')
        return [reply[1] for reply in varBinds]

    def get_pdu_group(self, pdu):
        pass

    def outlet_list(self, pdu):
        pass

    def group_outlets(self, outlets, groupname):
        pass

    def turn_off_outlet(self, pdu, outlet):
        """Turn the outlet on"""
        self._turn_outlet(pdu, outlet, 'off')

    def turn_on_outlet(self, pdu, outlet):
        """Turn the outlet on"""
        self._turn_outlet(pdu, outlet, 'on')

    def reboot_outlet(self, pdu, outlet):
        """Power cycle the outlet"""
        self._turn_outlet(pdu, outlet, 3)

    def _turn_outlet(self, pdu, outlet, status):
        """Private helper function to set a pdu to a given status. Statuses
        may be one of:
             * 0 = none
            * 1 = on
            * 2 = off
            * 3 = reboot"""
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdgen.setCmd(
            cmdgen.CommunityData('OSL_private'),
            cmdgen.UdpTransportTarget((pdu, self.port)),
            (cmdgen.MibVariable(
                'Sentry3',
                'outletControlAction',
                outlet.tower,
                outlet.infeed,
                outlet.outfeed),
                status)
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
