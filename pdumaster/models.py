import os
import collections

from pysnmp.entity.rfc3413.oneliner import cmdgen as cmdgenerator
from pysnmp.smi import builder
import toml

from pdumaster import pdu_exceptions

SENTRY_MIB_DIR = "%s/mib" % os.path.dirname(os.path.realpath(__file__))

Outlet = collections.namedtuple('outlet', ['tower', 'infeed', 'outfeed',], verbose=False)

def init_mib_builder(cmdgen, mib_dir=SENTRY_MIB_DIR):
    mib_builder = cmdgen.snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    sources = mib_builder.getMibSources() + (
        builder.DirMibSource(mib_dir),
    )
    mib_builder.setMibSources(*sources)
    mib_builder.loadModules('SNMPv2-MIB', 'IF-MIB', 'Sentry3')

    return mib_builder

def load_config(path):
    with open(path) as f:
        return update_config(toml.loads(f.read()))

def update_config(conf):
    """
    Go through all PDU configs and if their get/set communities aren't set, then
    use the global communities as fallback conf values.
    """
    pdu_globals = conf['pdumaster']
    set_community = pdu_globals.get("set_community", "")
    get_community = pdu_globals.get("get_community", "")
    for pdu in conf["pdus"]:
        if not 'set_community' in pdu:
            pdu['set_community'] = set_community
        if not 'get_community' in pdu:
            pdu['get_community'] = get_community
    return conf

class SentryPdu(object):
    """
    An object which provides an interface for interacting with a
    Power Distribution Unit. Not to be confused with a Protocol Data Unit.
    """

    def __init__(self, cmdgen, address="localhost", port=161, timeout=1, retries=5, set_community="", get_community=""):
        self.cmdgen = cmdgen
        self.transport = cmdgenerator.UdpTransportTarget((address, port), retries)
        self.set_community = cmdgenerator.CommunityData(set_community)
        self.get_community = cmdgenerator.CommunityData(get_community)

    def _check_errors(self, errorIndication, errorStatus, errorIndex, varBinds):
        if errorIndication or errorStatus:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            return varBinds

    def outletCommand(self, outlet, command):
        return cmdgenerator.MibVariable('Sentry3', command, *outlet)

    def _sendSetCommand(self, outlet, command, value):
        """Private function to send a given set command name to a pdu"""
        results = self.cmdgen.setCmd(self.set_community, self.transport,
            (self.outletCommand(outlet, command), value)
        )
        return self._check_errors(*results)

    def _sendGetCommand(self, outlet, command):
        """Private function to send a given get command name to a pdu"""
        results = self.cmdgen.getCmd(self.get_community, self.transport,
            self.outletCommand(outlet, command)
        )
        return self._check_errors(*results)

    def turn_outlet(self, outlet, status):
        command = 'outletControlAction'
        return self._sendSetCommand(outlet, command, status)


