import Pdu from pdumaster/pudmaster.py and initialize it
```
>>>from pdumaster.pudmaster import Pdu
>>>pdu_test = Pdu('ip_address_here',port,access_string)
```
Pdu object can be used to get various details like 

1) Number of towers
```
>>> print 'the number of towers are ' + str(pdu_test.get_num_towers())
```
2) Outlet oids and names
```
>>> oids , names = pdu_test.get_outlet_details()
>>> print oids , names
```
oids will the oids of all the outlets and names will the names of outlets

3) State of outlet from oid
  
  iterating through the oids returned from above function we can get states of all the outlets
```
>>>for i in range(len(oids)):
    state_dict = {'0':'off' , '1':'on' ,'2':'offwait' , '3':'onwait' , '4':'offerror' , '5':'onerror'}
    print names[i] + ' is ' + state_dict[str(pdu_test.state_from_oid(oids[i]))]
```
4) change state of outlet
```
>>>pdu_test.change_state('A',6,'off')
```
the format of change_state is change_state(tower_name,outlet_number,state)
vaild tower names are 'A' , 'B'
tower A has 8 outlets
tower B has 16 outlets 
vaild states are none , on , off , reboot

to reboot 3rd outlet of B tower you can use 
```
pdu_test.change_state('B',3,'reboot')
```