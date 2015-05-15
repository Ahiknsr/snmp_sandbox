from pysnmp import debug
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.smi import builder, view
import argparse
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

mibBuilder.loadModules('SNMPv2-MIB',  'Sentry3')

# the view controller is handy for viewing objects
mibViewController = view.MibViewController(mibBuilder)

class Pdu():


    def __init__(self,IP,PORT,ACCESS_STRING):
        self.ip = IP
        self.port = PORT
        self.access_string = ACCESS_STRING
        self.tower_number = '1.3.6.1.4.1.1718.3.1.4'
        self.outlet_list =  '1.3.6.1.4.1.1718.3.2.3.1.3'
        self.outlet_states = '1.3.6.1.4.1.1718.3.2.3.1.5'

    
    def nextCmd(self,oid):
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(self.access_string),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            oid
            )

        # Check for errors and print out results

        if errorIndication:
            print(errorIndication)
            return errorIndication
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
                return errorStatus
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        #print 'oid is ' + str(name) +'  ' + 'value is ' + str(val)
                        pass
                return varBindTable


    def getCmd(self,oid):
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
            cmdgen.CommunityData(self.access_string),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            oid
            )

        # Check for errors and print out results

        if errorIndication:
            print(errorIndication)
            return errorIndication
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
                return errorStatus
            else:
                #print varBindTable
                for oid , value in varBindTable:
                    #print value
                    return value
            

    def setCmd(self,oid,value):
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.setCmd(
            cmdgen.CommunityData(self.access_string),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            (cmdgen.MibVariable(oid),value)
            )

        # Check for errors and print out results

        if errorIndication:
            print(errorIndication)
            return errorIndication
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'))
                return errorStatus
            else:
                #print varBindTable
                for oid , value in varBindTable:
                    #print oid , value
                    return value


    def get_num_towers(self):

        IP= self.ip
        PORT= self.port

        for varBindTableRow in self.nextCmd(self.tower_number):
            for oid , value in varBindTableRow:
                return value


    def get_outlet_details(self):

        outlet_oids = []
        outlet_name = []
        for varBindTableRow in self.nextCmd(self.outlet_list):
            for oid , name in varBindTableRow:
                outlet_oids.append(str(oid))
                outlet_name.append(str(name))

        return outlet_oids , outlet_name


    def state_from_oid(self,OID):

        temp = OID.split('.')
        temp[-4] = '5'
        state_oid = '.'.join(temp)
        return self.getCmd(state_oid)


    def change_state(self,tower,outlet,state):

        tower_dict = { 'A':'1' , 'B':'2' , 'a':'1' , 'b':'2' }
        state_dict = { 'none': 0 , 'on' : 1 , 'off' : 2 , 'reboot' : 3 } 

        try:
            
            oid =  '1.3.6.1.4.1.1718.3.2.3.1.11.' + tower_dict[tower] + '.1.' + str(outlet) 
            return self.setCmd(oid,state_dict[state])

        except:

            return 'invalid data'


