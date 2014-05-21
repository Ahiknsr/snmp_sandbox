Designing PduMaster
===================

Goals:
------
* Be able to display data about pdu statuses in a human friendly form  
* Be able to turn off/on pdus and otherwise manipulate them  
* Recognize pdu groupings and types and react accordingly. For instance,
    recognize that two pdu outlets go to the same group, so when a machine
    needs to be rebooted all members of the group must be turned off.  

Interfaces:
-----------
* A scriptable cli  
* A curses admin interface (I may not be able to complete this)  
* Possibly a web front end  

Architecture:
-------------
We want a server application which runs on the internal network. This core 
application shall be known as `Pdu Master`. `Pdu Master` shall provide a simple,
well documented api for interacting with the pdus.
`Pdu Master` shall be interface agnostic.
`Pdu Master` will have a database of pdus to improve response times (the snmp 
protocol is slow).
`Pdu Master` will have a variety of functions to interact with the pdus over
snmp using the pysnmp library.

`Pdu Master` Database:
----------------------
There will be one table in the database called `pdus`. This table will have
the following columns:
TODO:finish listing tables
* name (string), part of the primary key. For example
* type (string), part of the primary key. For example

Configuration:
--------------
There will be two config files, both written in json.
TODO: go into greater depth about how the config files are written
