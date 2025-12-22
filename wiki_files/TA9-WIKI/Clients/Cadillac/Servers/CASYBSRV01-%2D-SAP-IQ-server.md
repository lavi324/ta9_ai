[[_TOC_]]

# Installation process
Environment: Centos 7 
Version: 16_1


##Download the installation file
[https://launchpad.support.sap.com/#/softwarecenter/template/products/_APP=00200682500000001943&_EVENT=NEXT&HEADER=Y&FUNCTIONBAR=Y&EVENT=TREE&NE=NAVIGATE&ENR=01200314690800002024&V=INST&TA=ACTUAL/SYBASE%20IQ]()


#Directory structure
/opt/application/ - holds the Sybase IQ software
/opt/logs/ – holds logfiles for the IQ instance and the for the catalog store
/opt/data/ – holds the dbspaces or symbolic links to raw devices.
/opt/archive/ - holds backups of the IQ database

# Update your system
`su - root`
`yum update -y`

# Configure user + environment
```
groupadd dba
useradd -g dba -s /bin/bash -d /home/iq16 iq16
passwd iq16
usermod -aG wheel iq16
chown -R iq16:dba /tmp/<YourPackage>
cd /opt/application/
mkdir iq16
chown -R iq16:dba iq16
su - iq16
```

# Extract the installation file
```
su - root
yum install epel-release unar csh file libaio libXext libXrender libXts libXi libstdc++ glibc.i686 glibc-devel -y
su - iq16
cd /tmp/
unar <YourPackage.rar>
cd /tmp/51052038/Sybase IQ Server 16.1/Linux on IA64 64bit
```


# Start Installation
![image.png](/.attachments/image-ed62803f-d0e1-49fe-a8f1-94520c8ab381.png)

**Install on:**
/opt/application/iq16/

![image.png](/.attachments/image-44cdc1be-5b25-44c3-acca-31e725618873.png)
![image.png](/.attachments/image-d938a843-a0a7-41b9-98a8-2f65f482f847.png)
![image.png](/.attachments/image-873e6efa-5ea6-471b-953b-f2c26649b0fc.png)
![image.png](/.attachments/image-2bf0adec-67fb-41c6-af9a-a80ed2db6ff2.png)
![image.png](/.attachments/image-4bb43af3-7f85-4ab4-b237-de0e55ddba0d.png)

Click next and pick you license accordingly.

# After installation completed

# Change root bashrc

`su - root`

`vi .bashrc`

**Add This**

```
# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
export SYBASE="/opt/application/iq16/"
```

## Change iq16 bashrc
`su - iq16`
`cd`
`vi .bashrc`
```
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
source /opt/application/iq16/IQ.sh
export IQ_USE_DIRECTIO=1
```


## Edit th IQ.sh file
`vi /opt/application/iq16/IQ.sh`

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

IQDIR16="/opt/application/iq16/IQ-16_1"

case "64" in
        *64)    IQ__BIN="${IQDIR16}/bin64"
                IQ__LIB="${IQDIR16}/lib64"
                ;;
        *)      IQ__BIN="${IQDIR16}/bin32"
                IQ__LIB="${IQDIR16}/lib32"
                ;;
esac

# ... Prepend to Path ..............................

PATH="${IQ__BIN}:${PATH}"

# ... Setup O/S specific variables .................

if [ "64" = AIX64 ]
then
        LIBPATH="${IQ__LIB}:$LIBPATH"
        export LIBPATH
else
        LD_LIBRARY_PATH="${IQ__LIB}:$LD_LIBRARY_PATH"
        export LD_LIBRARY_PATH
        if [ ! -z "${LD_LIBRARY_PATH_64:-}" ]
        then
            # This is required when installing with ASE 15.5
            LD_LIBRARY_PATH_64="${IQ__LIB}:$LD_LIBRARY_PATH_64"
            export LD_LIBRARY_PATH_64
        fi
fi


export IQDIR16 SYBROOT SYBASE SYBASE_JRE7_64 PATH

unset IQ__BIN IQ__LIB
```

## Restart the server

`sudo shutdown -r now`

# Start the database utility 

## make data directory
```
su - root
mkdir -p /opt/data/<DBNAME>
mkdir -p /opt/logs/<DBNAME>
mkdir -p /opt/archive/<DBNAME>
mkdir -p /tmpiq
chown -R iq16:dba /tmpiq
chown -R iq16:dba /opt/archive/<DBNAME>
chown -R iq16:dba /opt/logs/<DBNAME>
chown -R iq16:dba /opt/data/<DBNAME>
```

#Install Anaconda 3
```
wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
sudo sh Anaconda3-2019.07-Linux-x86_64.sh
sudo cp anaconda3/lib/libstdc++.so.6.0.26 /usr/lib64
sudo mv  /usr/lib64/libstdc++.so.6 /usr/lib64/libstdc++.so.6.orig
sudo ln -s /usr/lib64/libstdc++.so.6.0.26 /usr/lib64/libstdc++.so.6
conda config --set auto_activate_base false
```

# Create a Database:
`su - iq16`
`vi create_database.sql`

**Add This**
```
create database '/opt/data/<DBNAME>/<DBNAME>.db'
transaction log on '/opt/logs/<DBNAME>/<DBNAME>.log'
case ignore
collation 'UTF8BIN'
DBA USER 'DBA'
DBA PASSWORD 'Sap123'
blank padding on
jconnect on
iq path '/opt/data/<DBNAME>/IQ_SYSTEM_MAIN_01.iq'
iq size 20000
message path '/opt/logs/<DBNAME>/<DBNAME>.iqmsg'
temporary size 25000
;
```

##Create Database Space
`su - iq16`
`vi create_dbspace.sql`

**Add This**
```
create dbspace MAIN_DATA
using
file MAIN_DATA_01 '/opt/data/<DBNAME>/MAIN_DATA_01.iq' size 200000,
file MAIN_DATA_02 '/opt/data/<DBNAME>/MAIN_DATA_02.iq' size 200000,
file MAIN_DATA_03 '/opt/data/<DBNAME>/MAIN_DATA_03.iq' size 200000,
file MAIN_DATA_04 '/opt/data/<DBNAME>/MAIN_DATA_04.iq' size 200000,
file MAIN_DATA_05 '/opt/data/<DBNAME>/MAIN_DATA_05.iq' size 200000,
file MAIN_DATA_06 '/opt/data/<DBNAME>/MAIN_DATA_06.iq' size 200000,
file MAIN_DATA_07 '/opt/data/<DBNAME>/MAIN_DATA_07.iq' size 200000,
file MAIN_DATA_08 '/opt/data/<DBNAME>/MAIN_DATA_08.iq' size 200000;
```
##Create Database Space2
`vi alter_dbspace.sql`
**Add This**
```
alter dbspace IQ_SYSTEM_TEMP
add
file IQ_SYSTEM_TEMP_02 '/opt/data/dbtmp/<DBNAME>/IQ_SYSTEM_TEMP_02.iqtmp' size 25000,
file IQ_SYSTEM_TEMP_03 '/opt/data/dbtmp/<DBNAME>/IQ_SYSTEM_TEMP_03.iqtmp' size 25000,
file IQ_SYSTEM_TEMP_04 '/opt/data/dbtmp/<DBNAME>/IQ_SYSTEM_TEMP_04.iqtmp' size 25000;
```

# Start Database
`start_iq -n utility -su Sap123`

**server will run!!!**

## Attach database to it
`dbisql -c "uid=DBA;pwd=Sap123;dbn=utility_db" -nogui create_database.sql`

## Create and adjust IQ cinfiguration file

## Stop utility_db and start the database using the configuration file

`stop_iq`
`start_iq /opt/data/<DBNAME>/<DBNAME>.db -n <DBNAME>`

## Attach Space to it
`dbisql -c "uid=DBA;pwd=Sap123;srv=<DBNAME>" -nogui create_dbspace.sql`
`dbisql -c "uid=DBA;pwd=Sap123;srv=<DBNAME>" -nogui alter_dbspace.sql`

#Test connection:
`dbisql -c "uid=DBA;pwd=Sap123;srv=<DBNAME>" -nogui`


##Stop the server
`stop_iq`


# Make configuration file
cd /opt/data/<DBNAME>/
vi <DBNAME>.cfg
**Add This**
```
-n <DBNAME>
-iqmc 10000
-iqtc 10000
-iqlm 6000
-x "tcpip(port=2638)"
-c 128m
-m
-gm 100
-o /opt/data/<DBNAME>/<DBNAME>.srvlog
-os 10m
-zo /opt/logs/<DBNAME>/<DBNAME>.rlg
-zr SQL+HOSTVARS
-zs 10m
-zn 20
```

# Start the server with the new configuration:
cd /opt/data/<DBNAME>
`start_iq @<DBNAME>.cfg <DBNAME>.db`




# Configure auto startup
`su - root`
`vi /etc/systemd/system/<DBNAME>.service`
**Add This**
```
[Unit]
Description=IQ Service
After=network.target

[Service]
Type=forking
RemainAfterExit=yes
ExecStart=/usr/bin/su iq16 -c "source /opt/application/iq16/IQ.sh; /opt/application/iq16/IQ-16_1/bin64/start_iq @/opt/data/<DBNAME>/<DBNAME>.cfg /opt/data/<DBNAME>/<DBNAME>.db"
ExecStop=/usr/bin/su iq16 -c "source /opt/application/iq16/IQ.sh; /opt/application/iq16/IQ-16_1/bin64/stop_iq -stop one"

[Install]
WantedBy=multi-user.target
```
```

systemctl enable <DBNAME>.service
systemctl start <DBNAME>.service
```

# Add license 
```
put the file here
cd /opt/application/iq16/SYSAM-2_0/licenses/
```

# Change license configuration
```
cd /opt/application/iq16/IQ-16_1/Sysam/
vi iq.default.lmp
```

to this:
PE=EE
LT=AC

PE = Product edition
EE = Enterprise Edition 
AC =  OEM CPU License
LT = License Type


save and quit.
```
cd /opt/data/<DBNAME>/<DBNAME>.lmp
vi <DBNAME>.lmp
```
PE=EE
LT=AC

save and quit.