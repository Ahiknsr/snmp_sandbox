
from pysnmp import debug
#from pysnmp.smi import builder, view
from pysnmp.entity.rfc3413.oneliner import cmdgen

#thanks checkaa for the name
class pdu_device_whisperer:
    def __init__(self):
        #list of pdus TODO: make these be read from a config file
        self.pdus = ('pdu-b210-dell03.osuosl.oob', 'pdu-b210-dell13.osuosl.oob')
        pass

    def scan_pdus(self):
        for pdu in self.pdus:
            errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
                cmdgen.CommunityData('OSL_private'),
                cmdgen.UdpTransportTarget((pdu, port)),
                cmdgen.MibVariable('Sentry3',''),
                lookupNames=True, lookupValues=True, lexicographicMode=True,
                ignoreNonIncreasingOid=True
            )

        # Check for errors and print out results

        if errorIndication:
            #TODO: handle errors gracefully
            print(errorIndication)
            error += die
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
                #TODO: handle errors gracefully
                error += die
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        modName, symName, suffix = mibViewController.getNodeLocation((name))
                        print "%s - %s - %s - %s" % (pdu, symName, suffix, val)
                        print "-------"
                        #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


