from pysnmp import debug
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi import builder, view
import argparse
import tabulate

#debug.setLogger(debug.Debug('all'))
cmdGen = cmdgen.CommandGenerator()

# create MIB builder
mibBuilder = builder.MibBuilder().loadModules('SNMPv2-MIB', 'IF-MIB', 'Sentry3')

# the view controller is handy for viewing objects
mibViewController = view.MibViewController(mibBuilder)

# this sets a path where we can store our mib-file Sentry3.pyc
mibSources = mibBuilder.getMibSources() + (
                builder.DirMibSource('some/convenient/place'),
             )

mibBuilder.setMibSources(*mibSources)

# a list of pdu ips
ip_addresses = ('10.0.0.9', '10.0.0.13')

# a list of pdu ips
pdus = ('pdu-b210-dell03.osuosl.oob', 'pdu-b210-dell13.osuosl.oob')

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
