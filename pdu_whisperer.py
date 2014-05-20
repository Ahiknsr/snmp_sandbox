from collections import namedtuple

from pysnmp import debug
#from pysnmp.smi import builder, view
from pysnmp.entity.rfc3413.oneliner import cmdgen


pdu_data = namedtuple("pdu_data", ("modName", "symName", "suffix"))

#thanks checkaa for the name
class pdu_whisperer:
    def __init__(self, pdus):
        self.pdus = pdus

    def scan_pdus(self):
        """Scans all the pdus and returns a list of named tuples"""
        for pdu in self.pdus:
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
                        pdu_data_list.append(pdu_data(modName, symName, suffix))
                        #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        return pdu_data_list


