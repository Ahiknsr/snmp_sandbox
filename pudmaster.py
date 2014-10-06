from pysnmp import debug
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi import builder, view
import argparse
import tabulate
import os

#debug.setLogger(debug.Debug('all'))
cmdGen = cmdgen.CommandGenerator()

mibdir = "%s/mib" % os.path.dirname(os.path.realpath(__file__))

# create MIB builder
#mibBuilder = builder.MibBuilder()

mibBuilder = cmdGen.snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

# load mibs
mibSources = mibBuilder.getMibSources() + (builder.DirMibSource(mibdir),)
mibBuilder.setMibSources(*mibSources)

mibBuilder.loadModules('SNMPv2-MIB', 'IF-MIB', 'Sentry3')

# the view controller is handy for viewing objects
mibViewController = view.MibViewController(mibBuilder)

# a list of pdu ips

# a list of pdu ips
pdus = ('pdu-b210-dell65.osuosl.oob',)

# standard snmp port
port = 161

table_headers = ['PDU', 'Field']
"""
the following scans all the stuff on each ip address
"""
for pdu in pdus:

    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData('OSL_private'),
        cmdgen.UdpTransportTarget((pdu, port)),
        cmdgen.MibVariable('Sentry3',''),
        lookupNames=True, lookupValues=True, lexicographicMode=True,
        ignoreNonIncreasingOid=True
    )

    # Check for errors and print out results

    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    modName, symName, suffix = mibViewController.getNodeLocation((name))
                    print "%s - %s - %s - %s" % (pdu, symName, suffix, val)
                    print "-------"
                    #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


"""
The following sets the value of the outletcontrol action for outlet
4 on infeed 1 on tower 2 to "on", effectively turning the outlet on


errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('OSL_private'),
    cmdgen.UdpTransportTarget((ip_address, 161)),
    (cmdgen.MibVariable('Sentry3', 'outletControlAction', 2, 1, 4), 'on')
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
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

"""
