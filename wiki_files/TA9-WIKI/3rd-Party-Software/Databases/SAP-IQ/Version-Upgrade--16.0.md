
[[_TOC_]]
#   I.    Upgrading the Current SAP IQ Version

If you have already installed SAP IQ, before installing this update
enter the following command to verify that you are using the correct 
version of SAP IQ:
```
su - iq16
$IQDIR16/bin64/start_iq -v2
```
#   II.   Backup Notes
Back up your databases before installing this support package

#   III.  Installation and Upgrade
## * Preserving Modified Default Values

For each database, run sp_iqcheckoptions and capture the output before and after the upgrade. The sp_iqcheckoptions procedure lists current and default values of database and server startup options that have been changed from the default. The procedure output shows if any default values that you reset have changed in the new release, and records the values being used, so you can reset them after the upgrade.

Example:
[https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/439/sp_iqcheckoptions]()

![image.png](/.attachments/image-c4c1ec26-c880-4ae0-b8f9-17ba619cb89f.png)


## * License Validation

   The SAP IQ installer includes a step to verify that your license
   maintenance support is in compliance (or near compliance).  A server 
   that is more than 1 year out of maintenance will not run. Validating your 
   license(s) before you install this update ensures that your database 
   functions correctly after installation. A validation should be done 
   for each database on which this update will be applied.

   NOTICE: SAP IQ 16.0 SP11 and newer, includes a new version of SySAM(v2.4).
   If you are using an earlier version of the license server it must be 
   updated before installing this release to work correctly. Failure
   to update the license server, if in use, can result in the server not
   starting, with error message: FlexNet Licensing error:-5,414

   The SySAM server is included in the sysam_utilities directory of the
   install package.

##  * Upgrade Instructions
   
   This release of SAP IQ 16.0 SP11 PL27 does not support 
   rolling upgrades. 

1.	Open support.sap.com in a browser.
2.	Choose “Software Downloads”
3.	Log in with you S-user if required.
4.	Choose “Support Packages & Patches”
5.	Open “By Alphabetical Index (A-Z)”
6.	Choose “I”
7.	Choose “SYBASE IQ”
8.	Choose “SYBASE IQ 16.0”
9.	Choose “SYBASE IQ SERVER 16.0”
10.	In a combobox choose “LINUX ON X86_64 64BIT”
11.	Choose “IQSERV160011P_27-20011180.TGZ” and download it.

 
##   * Upgrading Simplex

###  1. Shut down all affected SAP IQ servers.
   See "Stopping Servers" in the SAP IQ Installation and Configuration 
   Guide.

###   2. Back up the databases and any modified files in the 
   $IQDIR16 directory.

###   3. Uninstall the current version of SAP IQ. See the SAP IQ 
   Installation and Configuration Guide for the uninstall process.

###   4. Install this update.

###   5. Verify that this support package has been installed correctly by 
   checking the version string of the server: start_iq -v2

###   6. Start the server and run ALTER DATABASE UPGRADE



# Start Installation

Log in to the Centos 7 machine.
switch user to iq16:
```su - iq16```

##Download the appropriate version of SapIQ 
See IQ process
```
[iq16@disybsrv02 ~]$ ps -ef | grep iq
iq16      8575     1  0 08:34 ?        00:00:04 /opt/application/iq16/IQ-16_0/bin64/iqsrv16 @/opt/data/ivoryiq/ivoryiq.cfg /opt/data/ivoryiq/ivoryiq.db -gc 20 -gd all -gl all -gp 4096 -ti 4400 -gn 105 -hn 5
root     18772 18702  0 08:45 pts/0    00:00:00 su - iq16
iq16     18774 18772  0 08:45 pts/0    00:00:00 -bash
iq16     18806 18774  0 08:45 pts/0    00:00:00 ps -ef
iq16     18807 18774  0 08:45 pts/0    00:00:00 grep --color=auto iq
```


##Check Version

```[iq16@disybsrv02 ~]$ iqsrv16 -v2iqsrv16 -v2```

###Output:
```
16.0.0.2805
SAP IQ/16.0.110.2805/11355/P/sp11.20/Enterprise Linux64 - x86_64 - 2.6.18-194.el5/64bit/2018-06-15 02:57:16
```

##switch to root:
```su - root```

##copy the tar file to /tmp

```cp IQSERV160011P_27-20011180.TGZ /tmp```


##Change file owner
```
cd /tmp
chown -R iq16:dba IQSERV160011P_27-20011180.TGZ
```

##Switch back to iq16
```
su - iq16
cd /tmp
```

##Extract the file: 
```
tar xvfz IQSERV160011P_27-20011180.TGZ
cd ebf29597/
```

##See Process of the server:
```ps -ef | grep iqsrv```

###Output:
```
iq16      8575     1  0 08:34 ?        00:00:05 /opt/application/iq16/IQ-16_0/bin64/iqsrv16 @/opt/data/ivoryiq/ivoryiq.cfg /opt/data/ivoryiq/ivoryiq.db -gc 20 -gd all -gl all -gp 4096 -ti 4400 -gn 105 -hn 5
iq16     19160 19077  0 08:50 pts/0    00:00:00 grep --color=auto iqsrv
```

##Test Login:

```[iq16@disybsrv02 ebf29597]$ dbisql -c "uid=dba;pwd=ivoryIQ\$#data;eng=ivoryiq" -nogui```

###Output:
```
(DBA)> sp_iqconnection;
          ConnHandle Name                                                                                                                                                                                                                                                            Userid                                                                                                                                                                                                                                                          LastReqTime                                                                                                                                                                                                                                                     ReqType                                                                                                                                                                                                                                                         IQCmdType                        LastIQCmdTime            IQCursors LowestIQCursorState  IQthreads                TxnID ConnCreateTime              TempTableSpaceKB      TempWorkSpaceKB             IQconnID         satoiq_count         iqtosa_count CommLink                                                                                                                                                                                                                                                        NodeAddr                                                                                                                                                                                                                                                           LastIdle MPXServerName                                                                                                                    LSName                                                                                                                                                                                                                                                          INCConnName                                                                                                                                                                                                                                                     INCConnSuspended
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          1000000004 INT: StmtPerfMngrConn                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           unknown (0)                                                                                                                                                                                                                                                     NONE                             0001-01-01 00:00:00.0            0 NONE                         0                    0 2020-10-18 08:34:41.0                      0                    0                    4                    2                    0 NA                                                                                                                                                                                                                                                              NA                                                                                                                                                                                                                                                                        0 (NULL)                                                                                                                           (NULL)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          N
                  13 SQL_DBC_2b164120bd0                                                                                                                                                                                                                                             DBA                                                                                                                                                                                                                                                             2020-10-18 08:49:34.788                                                                                                                                                                                                                                         PREFETCH                                                                                                                                                                                                                                                        NONE                             2020-10-18 08:49:34.0            1 END_OF_DATA                  0             73877293 2020-10-18 08:46:29.0                      0                  128                  386                   51                   72 TCPIP                                                                                                                                                                                                                                                           10.100.130.41                                                                                                                                                                                                                                                          8807 (NULL)                                                                                                                           (NULL)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          N
                  14 SQL_DBC_7fd6cc098e60                                                                                                                                                                                                                                            DBA                                                                                                                                                                                                                                                             2020-10-18 08:51:49.958                                                                                                                                                                                                                                         OPEN                                                                                                                                                                                                                                                            IQUTILITYOPENCURSOR              2020-10-18 08:51:49.0            0 NONE                         0             73877434 2020-10-18 08:51:45.0                      0                    0                  552                   48                    2 local                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   287 (NULL)                                                                                                                           (NULL)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          N
(3 rows)
Execution time: 0.035 seconds
```
##Exit and shutdown iq:
```
(DBA)> exit
[iq16@disybsrv02 ebf29597]$ stop_iq
```
**say yes to shut down.**

rename the current version to another folder name:
```
[root@disybsrv02 tmp]# cd /opt/application/
[root@disybsrv02 application]# mv iq16/ iq16_sp11_pl20
[root@disybsrv02 application]# mkdir iq16
[root@disybsrv02 application]# chown -R iq16:dba iq16
```

#Start sapIQ installation process
```
[root@disybsrv02 application]# su - iq16
[iq16@disybsrv02 ~]$ cd /tmp
[iq16@disybsrv02 tmp]$ cd ebf29597/
[iq16@disybsrv02 ebf29597]$ ./setup.bin -i console
Preparing to install...
Extracting the JRE from the installer archive...
Unpacking the JRE...
Extracting the installation resources from the installer archive...
Configuring the installer for this system's environment...
Launching installer...
===============================================================================
SAP IQ Server Suite                              (created with InstallAnywhere)
-------------------------------------------------------------------------------
Preparing CONSOLE Mode Installation...
===============================================================================
Title
-----
CONSOLE
PRESS <ENTER> TO CONTINUE:
===============================================================================
Introduction
------------
InstallAnywhere will guide you through the installation of SAP IQ Server Suite
16.0 sp11.27 (64-bit) .
It is strongly recommended that you quit all programs before continuing with
this installation.
Respond to each prompt to proceed to the next step in the installation.  If you
want to change something on a previous step, type 'back'.
You may cancel this installation at any time by typing 'quit'.
PRESS <ENTER> TO CONTINUE:
===============================================================================
Choose Install Folder
---------------------
Where would you like to install?
  Default Install Folder: /opt/application/iq16
ENTER AN ABSOLUTE PATH, OR PRESS <ENTER> TO ACCEPT THE DEFAULT
      :
===============================================================================
Choose Install Set
------------------
Please choose the Install Set to be installed by this installer.
  ->1- Typical
    2- Customize...
ENTER THE NUMBER FOR THE INSTALL SET, OR PRESS <ENTER> TO ACCEPT THE DEFAULT
   : 2
===============================================================================
Choose Product Features
-----------------------
ENTER A COMMA_SEPARATED LIST OF NUMBERS REPRESENTING THE FEATURES YOU WOULD
LIKE TO SELECT, OR DESELECT. TO VIEW A FEATURE'S DESCRIPTION, ENTER
'?<NUMBER>'.  PRESS <RETURN> WHEN YOU ARE DONE:
    1- [X] SAP IQ
    2-  |-[X] SAP IQ Server
    3-     |-[X] Additional Connectivity Language Modules
    4-  |-[X] SAP IQ Client
    5-  |-[X] SAP IQ Web Drivers
    6-  |-[X] SAP IQ ODBC Driver
    7- [ ] SAP Control Center
    8-  |-[ ] Management User Interface for SAP IQ
    9-  |-[ ] Remote Command and Control Agent for SAP IQ
   10- [X] Cockpit Framework
   11-  |-[X] SAP IQ Cockpit
   12-  |-[X] Remote Command and Control Agent for SAP IQ
   13- [X] jConnect 7.0 for JDBC
   14- [ ] SySAM License Server
   15- [X] SySAM License Utilities
Please choose the Features to be installed by this installer.:
===============================================================================
Software License Type Selection
-------------------------------
What would you like to do?
    1- Install licensed copy of SAP IQ Server Suite 16.0 sp11.27 (64-bit)
  ->2- Evaluate SAP IQ Server Suite 16.0 sp11.27 (64-bit)
Enter one of the options above: 
===============================================================================
End-user License Agreement
--------------------------
1)  Americas and Asia Pacific                    2)  Argentina
3)  Asia Pacific Region - General                4)  Australia
5)  Belgium(English)                             6)  Brazil
7)  Canada                                       8)  Denmark
9)  Europe,Middle East, and Africa - General     10) France(English)
11) France(French)                               12) Germany(English)
13) Hong Kong                                    14) India
15) Italy(English)                               16) Italy(Italian)
17) Japan                                        18) Korea
19) Latin America Countries - Other than Argent  20) Malaysia
21) Mexico                                       22) Netherlands
23) New Zealand                                  24) Norway
25) People's Republic of China(PRC)              26) Singapore
27) South Africa                                 28) Spain(English)
29) Spain(Spanish)                               30) Sweden
31) Switzerland(English)                         32) Taiwan
33) United Kingdom                               34) United States of America
35) Any Other Locations
Please enter the number of the location you are installing. (1-35) (Default:
   1): 35
LICENSE AGREEMENT
General (applies to all countries,
except those for which a specific
country/language version is posted)
IMPORTANT NOTICE: READ THIS LICENSE AGREEMENT CAREFULLY
BEFORE USING THE ENCLOSED PROGRAM.  YOU MAY USE THE PROGRAM
ACQUIRED ONLY IN THE COUNTRY IN WHICH THIS LICENSE WAS
ACCEPTED, AND ONLY IN ACCORDANCE WITH THE FOLLOWING TERMS
AND CONDITIONS.  IF YOU DO NOT AGREE TO BE BOUND BY THESE
TERMS, YOU MAY NOT USE THE PROGRAM. BY DOWNLOADING,
INSTALLING, OR USING THE PROGRAM IN ANY WAY, YOU ACKNOWLEDGE
THAT YOU HAVE READ, UNDERSTAND AND AGREE TO THE TERMS OF
THIS AGREEMENT.  IF YOU DO NOT AGREE WITH THESE TERMS,
PRESENT YOUR RECEIPT OR OTHER PROOF OF PURCHASE, TOGETHER
WITH THE PROGRAM MEDIA, DOCUMENTATION AND PACKAGING (IF ANY)
TO THE ENTITY FROM WHICH YOU OBTAINED THIS PRODUCT WITHIN 30
DAYS TO REQUEST A REFUND.  THIS IS A LICENSE AND NOT A SALE.
Press ENTER to read the text [Type 'back' and press ENTER to skip the text]
   : back
I agree to the terms of the SAP license for the install location specified.
   (Y/N): Y
===============================================================================
SySAM License
-------------
Enter the SAP IQ Server Suite 16.0 sp11.27 (64-bit)  license key(s) or specify
the license server where license key(s) were previously deployed.
    1- Specify license keys
    2- Use previously deployed license server
  ->3- Continue installation without a license key
Enter one of the options above:
===============================================================================
Product Licenses
----------------
Please select the product edition and license type you would like to configure.
Product Edition
  ->1- Enterprise Edition (EE)
    2- Small Business Edition (SE)
    3- Express Edition (XE)
    4- Single Application Edition (SA)
    5- Unknown
Enter one of the options above:
License Type
    1- CPU License (CP)
  ->2- CPU Development and Test License (DT)
    3- Standby CPU License (SF)
    4- OEM CPU License (AC)
    5- OEM Standby CPU License (BC)
    6- Unknown
Enter one of the options above: 4
===============================================================================
SySAM Notification
------------------
Please configure the SySAM email alert mechanism.  When configured, specified
recipients will receive email notifications about SySAM events that may need
administrator attention.
Do you want to configure email alerts? (Y/N): N
===============================================================================
Pre-Installation Summary
------------------------
Please Review the Following Before Continuing:
Product Name:
    SAP IQ Server Suite 16.0 sp11.27 (64-bit)
Install Folder:
    /opt/application/iq16
Product Features:
    SAP IQ,
    SAP IQ Server,
    Additional Connectivity Language Modules,
    SAP IQ Client,
    SAP IQ Web Drivers,
    SAP IQ ODBC Driver,
    Cockpit Framework,
    SAP IQ Cockpit,
    Remote Command and Control Agent for SAP IQ,
    jConnect 7.0 for JDBC,
    SySAM License Utilities
Disk Space Information (for Installation Target):
    Required:  1,193,581,669 Bytes
    Available: 15,939,604,480 Bytes
PRESS <ENTER> TO CONTINUE:
===============================================================================
Ready To Install
----------------
InstallAnywhere is now ready to install SAP IQ Server Suite 16.0 sp11.27
(64-bit)  onto your system at the following location:
   /opt/application/iq16
PRESS <ENTER> TO INSTALL:
===============================================================================
Installing...
-------------
 [==================|==================|==================|==================]
 [------------------|------------------|------------------|------------------]
===============================================================================
Cockpit - Configure HTTP/HTTPS Ports
------------------------------------
Cockpit needs HTTP/HTTPS ports that do not conflict with ports used by other
applications and services on this system. Accept the default ports or specify
other, unused ports.
HTTP Port: [integer (1025-65535)] (Default: 4282):
HTTPS Port: [integer (1025-65535)] (Default: 4283):
===============================================================================
Cockpit - Configure RMI Port
----------------------------
The RMI service needs to use a port that is not used by other applications or
services on this system. Accept the default port or specify an unused port.
RMI Port: [integer (1025-65535)] (Default: 4992):
===============================================================================
Cockpit - Configure TDS Port
----------------------------
The TDS service needs to use a port that is not used by other applications or
services on this system. Accept the default port or specify an unused port.
TDS Port: [integer (1025-65535)] (Default: 4998):
===============================================================================
Start Cockpit
-------------
Do you want to start Cockpit Server?
  ->1- Yes
    2- No
Enter one of the options above: 2
===============================================================================
Install Complete
----------------
The installation was successful. SAP IQ Server Suite 16.0 sp11.27 (64-bit)  has
been installed to:
/opt/application/iq16
Would you like to launch the SAP Product Download Center website? (Y/N): N
```

#Edit IQ.sh

```
[iq16@disybsrv02 ~]$ cd /opt/application/iq16
[iq16@disybsrv02 iq16]$ vi IQ.sh
```
##Should look like this:

```

#!/bin/sh
# ------------------------------------------------------------
# IQ-16_0.sh            10/25/2011              Sybase, Inc.
# ------------------------------------------------------------
# Setup IQ environment for the 'bourne', 'korn' and 'bash'
# ------------------------------------------------------------
#     ** THIS FILE MUST BE SOURCED TO SET ENVIRONMENT **
# ------------------------------------------------------------

# ... Setup Sybase and SCJ environment .............

if [ -x /opt/application/iq16/SYBASE.sh ]
then
#       echo Sourcing SYBASE.sh
        . /opt/application/iq16/SYBASE.sh
fi

if [ -z "${SYBASE:-}" ]
then
        SYBASE="/opt/application/iq16"
fi

#Reset SYBROOT for IQ 16.0 use
SYBROOT="/opt/application/iq16"

if [ -z "${SYBASE_JRE7_64:-}" ]
then
        SYBASE_JRE7_64="$SAP_JRE7"
fi

# ... Optional directory for log files .............
#
# IQLOGDIR16="<Logging Directory>" ; export IQLOGDIR16
#
# ... Setup IQ environment .........................

IQDIR16="/opt/application/iq16/IQ-16_0"

case "64" in
        *64)    IQ__BIN="${IQDIR16}/bin64"
                IQ__LIB="${IQDIR16}/lib64"
                ;;
        *)      IQ__BIN="${IQDIR16}/bin32"
                IQ__LIB="${IQDIR16}/lib32"
                ;;
esac

# ... Prepend to Path ..............................
```

# Copy the license file from the backup we created:
```
[iq16@disybsrv02 iq16]$ cd ../iq16_sp11_pl20/SYSAM-2_0/licenses/
[iq16@disybsrv02 licenses]$ ls -l
total 4
-rw-r--r--. 1 iq16 dba 1628 Nov  1  2018 ANY_20181031_153313.lic
-rw-r--r--. 1 iq16 dba    0 Nov 15  2016 empty
[iq16@disybsrv02 licenses]$ cp ANY_20181031_153313.lic /opt/application/iq16/SYSAM-2_0/licenses/
```

#Check sapIQ version:
```iqsrv16 -v2```
###Output:
```
16.0.0.3463
SAP IQ/16.0.110.3463/14645/P/sp11.27/Enterprise Linux64 - x86_64 - 2.6.18-194.el5/64bit/2020-07-24 01:38:33
```

##Test if server is ready:
```
[iq16@disybsrv02 application]$ cd /opt/data/ivoryiq
[iq16@disybsrv02 ivoryiq]$ ls
IQ_SYSTEM_MAIN_01.iq  ivoryiq.db   MAIN_DATA_01.iq  MAIN_DATA_03.iq  MAIN_DATA_05.iq  MAIN_DATA_07.iq
ivoryiq.cfg           ivoryiq.lmp  MAIN_DATA_02.iq  MAIN_DATA_04.iq  MAIN_DATA_06.iq  MAIN_DATA_08.iq
[iq16@disybsrv02 ivoryiq]$ pwd
/opt/data/ivoryiq
[iq16@disybsrv02 ivoryiq]$ start_iq @/opt/data/ivoryiq/ivoryiq.cfg /opt/data/ivoryiq/ivoryiq.db
```

###Output:
```
Starting server ivoryiq on disybsrv02 at port 2638 (10/18 09:08:01)

Run Directory       : /opt/data/ivoryiq
Server Executable   : /opt/application/iq16/IQ-16_0/bin64/iqsrv16
Server Output Log   : /opt/log/ivoryiq/ivoryiq.srvlog
Server Version      : 16.0.110.3463/sp11.27
Open Client Version : 15.7
User Parameters     : '@/opt/data/ivoryiq/ivoryiq.cfg' '/opt/data/ivoryiq/ivoryiq.db'
Default Parameters  : -gc 20 -gd all -gl all -gp 4096 -ti 4400 -gn 105

I. 10/18 09:08:02. SAP IQ
I. 10/18 09:08:02. Version 16.0
I. 10/18 09:08:02. (64bit mode)
I. 10/18 09:08:02. Copyright 1992-2020 by SAP AG or an SAP affiliate company. All rights reserved
I. 10/18 09:08:02. Copyright (c) 2020 SAP AG or an SAP affiliate company.
I. 10/18 09:08:02. All rights reserved.
I. 10/18 09:08:02. Use of this software is governed by the SAP Software Use Rights Agreement.
I. 10/18 09:08:02. Refer to http://www.sap.com/about/agreements.html.
I. 10/18 09:08:02.
I. 10/18 09:08:02. Processors detected: 2 (containing 12 logical processors)
I. 10/18 09:08:02. Maximum number of processors the server will use: 2 physical processor(s), 12 core(s)
I. 10/18 09:08:02. Running Linux 3.10.0-957.21.3.el7.x86_64 #1 SMP Tue Jun 18 16:35:19 UTC 2019 on X86_64
I. 10/18 09:08:02. Server built for X86_64 processor architecture
I. 10/18 09:08:02. 131072K of memory used for caching
I. 10/18 09:08:02. Minimum cache size: 131072K, maximum cache size: 262144K
I. 10/18 09:08:02. Using a maximum page size of 4096 bytes
I. 10/18 09:08:02. Multiprogramming level: 105
I. 10/18 09:08:02. Warning: -gn value of 105 is too low for -gm value of 100
I. 10/18 09:08:02. Automatic tuning of multiprogramming level is disabled
=============================================================
IQ server starting with:
    100 connections         (       -gm )
     34 cmd resources       ( -iqgovern )
    749 threads             (     -iqmt )
    512 Kb thread stack size   (   -iqtss  )
  383488 Kb thread memory size ( -iqmt * -iqtss )
     12 IQ number of cpus  ( -iqnumbercpus )
     50 MB maximum size of IQMSG file ( -iqmsgsz )
     10 copies of IQMSG file archives ( -iqmsgnum )
I. 10/18 09:08:03. Starting database "ivoryiq" (/opt/data/ivoryiq/ivoryiq.db) at Sun Oct 18 2020 09:08
I. 10/18 09:08:03. Transaction log: /opt/log/ivoryiq/ivoryiq.log
I. 10/18 09:08:03. Starting checkpoint of "ivoryiq" (ivoryiq.db) at Sun Oct 18 2020 09:08
I. 10/18 09:08:03. Finished checkpoint of "ivoryiq" (ivoryiq.db) at Sun Oct 18 2020 09:08
I. 10/18 09:08:04. Update previous log GUID to: 14c92b30-dddb-11e8-8000-d7609babd14f
Update current log GUID to :6dfbcd0e-1121-11eb-8000-951132c87340
I. 10/18 09:08:04. Database "ivoryiq" (ivoryiq.db) started at Sun Oct 18 2020 09:08
I. 10/18 09:08:04. IQ Server ivoryiq.
I. 10/18 09:08:04. Starting checkpoint of "ivoryiq" (ivoryiq.db) at Sun Oct 18 2020 09:08
I. 10/18 09:08:04. Finished checkpoint of "ivoryiq" (ivoryiq.db) at Sun Oct 18 2020 09:08
I. 10/18 09:08:04. Database server started at Sun Oct 18 2020 09:08
I. 10/18 09:08:04. Trying to start SharedMemory link ...
I. 10/18 09:08:04.     SharedMemory link started successfully
I. 10/18 09:08:04. Trying to start TCPIP link ...
I. 10/18 09:08:04. Starting on port 2638
I. 10/18 09:08:09.     TCPIP link started successfully
I. 10/18 09:08:09. Now accepting requests
New process id is 30525
Server started successfully
```
#Login to the server:

[iq16@disybsrv02 ivoryiq]$ dbisql -c "uid=dba;pwd=ivoryIQ\$#data;eng=ivoryiq" -nogui

##Tell the server about the upgrade:

```(DBA)> alter database upgrade;```

###Output:

```
Database upgrade started
Creating system views
Creation of system views completed
Creating DBO views
Creation of DBO views completed
Creating system procedures
Creation of system procedures completed
Creating system views
Creation of system views completed
Setting option values
Setting option values completed
Creating migration procedures
Creation of migration procedures completed
Creating jConnect procedures
Creation of jConnect procedures completed
29 row(s) affected
Execution time: 3.154 seconds
```

##Check Status of the database:

```(DBA)> sp_iqstatus;```

###Output:
```
Name                                                                                                                                                                                                                                                            Value                                                                                                                     
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SAP IQ (TM)                                                                                                                                                                                                                                                     Copyright (c) 1992-2020 by SAP AG or an SAP affiliate company. All rights reserved.                                       
 Version:                                                                                                                                                                                                                                                       16.0.110.3463/14645/P/sp11.27/Enterprise Linux64 - x86_64 - 2.6.18-194.el5/64bit/2020-07-24 01:38:33                      
 Time Now:                                                                                                                                                                                                                                                      2020-10-18 09:08:50.044                                                                                                   
 Build Time:                                                                                                                                                                                                                                                    2020-07-24 01:38:33                                                                                                       
 File Format:                                                                                                                                                                                                                                                   23 on 03/18/1999                                                                                                          
 Server mode:                                                                                                                                                                                                                                                   IQ Server                                                                                                                 
 Catalog Format:                                                                                                                                                                                                                                                2                                                                                                                         
 Stored Procedure Revision:                                                                                                                                                                                                                                     1                                                                                                                         
 Page Size:                                                                                                                                                                                                                                                     131072/8192blksz/16bpp                                                                                                    
 Number of Main DB Files:                                                                                                                                                                                                                                       9                                                                                                                         
 Main Store Out Of Space:                                                                                                                                                                                                                                       N                                                                                                                         
 Number of Cache Dbspace Files:                                                                                                                                                                                                                                 0                                                                                                                         
 Number of Shared Temp DB Files:                                                                                                                                                                                                                                0                                                                                                                         
 Shared Temp Store Out Of Space:                                                                                                                                                                                                                                N                                                                                                                         
 Number of Local Temp DB Files:                                                                                                                                                                                                                                 4                                                                                                                         
 Local Temp Store Out Of Space:                                                                                                                                                                                                                                 N                                                                                                                         
 DB Blocks: 1-2560000                                                                                                                                                                                                                                           IQ_SYSTEM_MAIN                                                                                                            
 DB Blocks: 3136320-28736319                                                                                                                                                                                                                                    MAIN_DATA_01                                                                                                              
 DB Blocks: 29272320-54872319                                                                                                                                                                                                                                   MAIN_DATA_02                                                                                                              
 DB Blocks: 55408320-81008319                                                                                                                                                                                                                                   MAIN_DATA_03                                                                                                              
 DB Blocks: 81544320-107144319                                                                                                                                                                                                                                  MAIN_DATA_04                                                                                                              
 DB Blocks: 107680320-133280319                                                                                                                                                                                                                                 MAIN_DATA_05                                                                                                              
 DB Blocks: 133816320-159416319                                                                                                                                                                                                                                 MAIN_DATA_06                                                                                                              
 DB Blocks: 159952320-185552319                                                                                                                                                                                                                                 MAIN_DATA_07                                                                                                              
 DB Blocks: 186088320-211688319                                                                                                                                                                                                                                 MAIN_DATA_08                                                                                                              
 Local Temp Blocks: 1-3200000                                                                                                                                                                                                                                   IQ_SYSTEM_TEMP                                                                                                            
 Local Temp Blocks: 4181760-7381759                                                                                                                                                                                                                             IQ_SYSTEM_TEMP_02                                                                                                         
 Local Temp Blocks: 8363520-11563519                                                                                                                                                                                                                            IQ_SYSTEM_TEMP_03                                                                                                         
 Local Temp Blocks: 12545280-15745279                                                                                                                                                                                                                           IQ_SYSTEM_TEMP_04                                                                                                         
 Create Time:                                                                                                                                                                                                                                                   2018-11-01 13:26:35.007                                                                                                   
 Update Time:                                                                                                                                                                                                                                                   2020-10-18 09:08:10.000                                                                                                   
 Main IQ Buffers:                                                                                                                                                                                                                                               79553, 10000Mb                                                                                                            
 Temporary IQ Buffers:                                                                                                                                                                                                                                          79553, 10000Mb                                                                                                            
 LOAD IQ Buffers:                                                                                                                                                                                                                                               2048, 0Mb                                                                                                                 
 Main IQ Blocks Used:                                                                                                                                                                                                                                           11708165 of 207334400, 5%=89Gb, Max Block#: 187780952                                                                     
 Cache Dbspace IQ Blocks Used:                                                                                                                                                                                                                                  0 of 0, 0%=0Mb, Max Block#: 0                                                                                             
 Shared Temporary IQ Blocks Used:                                                                                                                                                                                                                               0 of 0, 0%=0Mb, Max Block#: 0                                                                                             
 Local Temporary IQ Blocks Used:                                                                                                                                                                                                                                548 of 12768000, 0%=4Mb, Max Block#: 0                                                                                    
 Main Reserved Blocks Available:                                                                                                                                                                                                                                25600 of 25600, 100%=200Mb                                                                                                
 Shared Temporary Reserved Blocks Available:                                                                                                                                                                                                                    0 of 0, 0%=0Mb                                                                                                            
 Local Temporary Reserved Blocks Available:                                                                                                                                                                                                                     32000 of 32000, 100%=250Mb                                                                                                
 IQ Dynamic Memory:                                                                                                                                                                                                                                             Current: 20384mb, Max: 20458mb                                                                                            
 Main IQ Buffers:                                                                                                                                                                                                                                               Used: 417, Locked: 0                                                                                                      
 Temporary IQ Buffers:                                                                                                                                                                                                                                          Used: 34, Locked: 0                                                                                                       
 LOAD IQ Buffers:                                                                                                                                                                                                                                               Used: 0, Locked: 0                                                                                                        
 Main IQ I/O:                                                                                                                                                                                                                                                   I: L2110/P411 O: C6/D412/P206 D:3 C:99.5                                                                                  
 Temporary IQ I/O:                                                                                                                                                                                                                                              I: L473/P0 O: C34/D50/P34 D:0 C:100.0                                                                                     
 Other Versions:                                                                                                                                                                                                                                                0 = 0Mb                                                                                                                   
 Active Txn Versions:                                                                                                                                                                                                                                           0 = C:0Mb/D:0Mb                                                                                                           
 Last Full Backup ID:                                                                                                                                                                                                                                           73812920                                                                                                                  
 Last Full Backup Time:                                                                                                                                                                                                                                         2020-10-17 01:26:32                                                                                                       
 Last Backup ID:                                                                                                                                                                                                                                                73812920                                                                                                                  
 Last Backup Type:                                                                                                                                                                                                                                              FULL                                                                                                                      
 Last Backup Time:                                                                                                                                                                                                                                              2020-10-17 01:26:32                                                                                                       
 DB Updated:                                                                                                                                                                                                                                                    1                                                                                                                         
 Blocks in next ISF Backup:                                                                                                                                                                                                                                     57263 Blocks: =447Mb                                                                                                      
 Blocks in next ISI Backup:                                                                                                                                                                                                                                     57263 Blocks: =447Mb                                                                                                      
 IQ large memory space:                                                                                                                                                                                                                                         6000Mb                                                                                                                    
 IQ large memory flexible percentage:                                                                                                                                                                                                                           50                                                                                                                        
 IQ large memory flexible used:                                                                                                                                                                                                                                 0Mb                                                                                                                       
 IQ large memory inflexible percentage:                                                                                                                                                                                                                         90                                                                                                                        
 IQ large memory inflexible used:                                                                                                                                                                                                                               0Mb                                                                                                                       
 IQ large memory anti-starvation percentage:                                                                                                                                                                                                                    50                                                                                                                        
 DB File Encryption Status:                                                                                                                                                                                                                                     OFF                                                                                                                       
 RLV Status:                                                                                                                                                                                                                                                    RW                                                                                                                        
 RLV memory limit (mb):                                                                                                                                                                                                                                         2048                                                                                                                      
 RLV memory used (bytes):                                                                                                                                                                                                                                       0                                                                                                                         
 RLV Log Buffers Allocated:                                                                                                                                                                                                                                     0                                                                                                                         
 RLV Log Buffers Globally Free:                                                                                                                                                                                                                                 0                                                                                                                         
 RLV Log Buffers Privately Free:                                                                                                                                                                                                                                0                                                                                                                         
 RLV Log Buffers In Use:                                                                                                                                                                                                                                        0                                                                                                                         

(71 rows)

Execution time: 0.035 seconds
```

done.

