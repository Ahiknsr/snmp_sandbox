Designing The PduMaster Library
===============================

Goals:
------
* Be able to display data about pdu statuses in a human friendly form  
* Be able to turn off/on pdus and otherwise manipulate them  
* Recognize pdu groupings and types and react accordingly. For instance,
    recognize that two pdu outlets go to the same group, so when a machine
    needs to be rebooted all members of the group must be turned off.  

Planned Interfaces:
-------------------
All interfaces will communicate with a server named `Pdu Server`, possibly 
written using flask.
`Pdu Server` will run on larch and respond to json api calls.
This server will user this `Pdu Master` library to communicate with the pdus and
database. All interfaces would require an API key or LDAP authenication with
`Pdu Server`.  
Proposed interfaces follow:
* A scriptable command line interface.  
* A curses admin interface.  
* An http web front end. This may or may not be part of `Pdu Server`.  

Architecture:
-------------
We want an application which runs on the internal network on `larch`. 
The core library to handle pysnmp and database requests shall be known as
`Pdu Master`, and shall be written in python 2.7.
`Pdu Master` shall provide a simple, well documented python api for interacting
with the pdus. `Pdu Master` shall be interface agnostic.
To be clear, `Pdu Master` is not a server, but rather a core library to be used
by `Pdu Server`.

`Pdu Master` will have a database of pdus. Pdu existance will be cached to avoid
querying for pdu data every time `Pdu Master` starts up. 
`Pdu Master` will have a variety of functions to interact with the pdus over
snmp using the pysnmp library. Funtions will include:
    * status reporting
    * per port power control
    * reboot

`Pdu Master` Database:
----------------------
There will be one table in the database called `pdus`. This table will have
the following columns:
* name (string), part of the primary key. The hostname of the pdu.
* type (string), part of the primary key. The type of pdu, such as `Sentry3`.
* label (string), a human readable label describing the pdu.
* group (string), a description of what groups this pdu belongs to.
* last_updated (datetime object), when the data on this pdu was last updated.

Configuration:
--------------
There will be two config files, both written in json.
The application level config will be called `pdumaster.json`, and shall reside
in the same directory of the application. The pdus file name is configurable,
but by default is `pdu_config.json`.
`pdu_config.json` is a simple hash table of pdu names and types. An example
folows.  

```
{
    "pdu-b210-dell03.osuosl.oob":"Sentry3",
    "pdu-b210-dell13.osuosl.oob":"Sentry3"
}

```

`pdumaster.json` has the following attributes:
* `db_engine`: Specifies the name of the database engine, if it runs separately
from the core app.  
A sample configuration follows:  
```
{
    "db_engine":null
}
```

Comments About Each File:
-------------------------
* DESIGN.md: This design document. Explains the state of the project and the path
* forwards.  
* LICENSE: The Apache 2.0 License.  
* app_config.py: Reads and parses the application level config named
* pdumaster.json.  
* curses_cli.py: A crude start on a curses ui.  
* db_model.py: A methods for manipulating pdus in the database.  
* mib/Sentry3.py: A mib file with definitions for communicating with Sentry3
* Pdus  
* pdu_config.json: A dictionary of pdus and their types.  
* pdu_config.py: Reads and parses pdu_config.json.  
* pdu_model.py: A model for the pdus table in the database.  
* pdu_whisperer.py: The part for communicating over snmp with the pdus.  
* pdumaster.json: The application level configuration.  
* pdumaster.py: The heart of the application.  
* pudmaster.py: Early development of the app.  
* The refs folder contains mib definitions and python files representing the mibs.
* requirements.txt: pip installable python dependancies.  


Feature Requests:
-----------------
`Pdu Master` related feature requests:
* Racktables integration  

The following features are requested for the forthcoming `Pdu Server`:
* Logs of what anyone touches with `Pdu Master`  
* A curses UI  
* A web interface  
