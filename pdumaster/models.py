import os
import collections

from pysnmp.entity.rfc3413.oneliner import cmdgen as cmdgenerator
from pysnmp.smi import builder
import toml

from pdumaster import pdu_exceptions

SENTRY_MIB_DIR = "%s/mib" % os.path.dirname(os.path.realpath(__file__))

Outlet = collections.namedtuple('outlet', ['tower', 'infeed', 'outfeed'])


def init_mib_builder(cmdgen, mib_dir=SENTRY_MIB_DIR):
    mib_builder = cmdgen.snmpEngine.msgAndPduDsp.mibInstrumController.\
        mibBuilder

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
    Go through all PDU configs and if their get/set communities aren't set,
    then use the global communities as fallback conf values.
    """
    pdu_globals = conf['pdumaster']
    set_community = pdu_globals.get("set_community", "")
    get_community = pdu_globals.get("get_community", "")
    for pdu in conf["pdus"]:
        if 'set_community' not in pdu:
            pdu['set_community'] = set_community
        if 'get_community' not in pdu:
            pdu['get_community'] = get_community
    return conf


class SnmpWrapper(object):
    """
    Wraps SNMP commands in an easier to use interface.
    """

    def __init__(self, cmdgen, address="localhost", port=161, timeout=1,
                 retries=5, set_community="", get_community=""):
        self.cmdgen = cmdgen
        self.transport = cmdgenerator.UdpTransportTarget(
            (address, port), retries)
        self.set_community = cmdgenerator.CommunityData(set_community)
        self.get_community = cmdgenerator.CommunityData(get_community)

    def _check_errors(self, errorIndication, errorStatus,
                      errorIndex, varBinds):
        if errorIndication or errorStatus:
            raise pdu_exceptions.SnmpActivationError(errorStatus, errorIndex)
        else:
            return varBinds

    def set_command_args(self, *args, **kwargs):
        raise NotImplementedError()

    def get_command_args(self, *args, **kwargs):
        raise NotImplementedError()

    def sendSetCommand(self, *args, **kwargs):
        """Private function to send a given set command name to a pdu"""
        results = self.cmdgen.setCmd(
            self.set_community, self.transport,
            self.set_command_args(*args, **kwargs)
        )
        return self._check_errors(*results)

    def sendGetCommand(self, *args, **kwargs):
        """Private function to send a given get command name to a pdu"""
        results = self.cmdgen.getCmd(
            self.get_community, self.transport,
            self.get_command_args(*args, **kwargs)
        )
        return self._check_errors(*results)


class SentryPdu(SnmpWrapper):

    def set_command_args(self, outlet, command, value, *args, **kwargs):
        return (self.outletCommand(outlet, command), value)

    def get_command_args(self, outlet, command, *args, **kwargs):
        return self.outletCommand(outlet, command)

    def outletCommand(self, outlet, command):
        return cmdgenerator.MibVariable('Sentry3', command, *outlet)

    def turn_outlet(self, outlet, status):
        command = 'outletControlAction'
        return self.sendSetCommand(outlet, command, status)

