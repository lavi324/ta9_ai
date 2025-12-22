#Introduction
OrientDB has a multi-master distributed architecture (called also as "master-less") where each server can read and write. Starting from v2.1, OrientDB support the role of "REPLICA", where the server is in read-only mode, accepting only idempotent commands, like Reads and Query. Furthermore when the server joins the distributed cluster as "REPLICA", own record clusters are not created like does the "MASTER" nodes.

Starting from v2.2, the biggest advantage of having many REPLICA servers is that they don't concur in writeQuorum, so if you have 3 MASTER servers and 100 REPLICA servers, every write operation will be replicated across 103 servers, but the majority of the writeQuorum would be just 2, because given N/2+1, N is the number of MASTER servers. In this case after the operation is executed locally, the server coordinator of the write operation has to wait only for one more MASTER server.

#Installation:
The installation process is the same as the single-node application. If this new server, got to next wiki [OrientDb](/TA9-WIKI/3rd-Party-Software/Databases/OrientDB).

Unlike the standard standalone deployment of OrientDB, there is a different script that you need to use when launching a distributed server instance. Instead of server.sh, you use dserver.sh. In the case of Windows, use dserver.bat. Whichever you need, you can find it in the bin of your installation directory.

$ ./bin/dserver.sh
Bear in mind that OrientDB uses the same orientdb-server-config.xml configuration file, regardless of whether it's running as a server or distributed server. For more information, see Distributed Configuration.

The first time you start OrientDB as a distributed server, it generates the following output:

+---------------------------------------------------------------+
|         WARNING: FIRST DISTRIBUTED RUN CONFIGURATION          |
+---------------------------------------------------------------+
| This is the first time that the server is running as          |
| distributed. Please type the name you want to assign to the   |
| current server node.                                          |
|                                                               |
| To avoid this message set the environment variable or JVM     |
| setting ORIENTDB_NODE_NAME to the server node name to use.    |
+---------------------------------------------------------------+

Node name [BLANK=auto generate it]:
You need to give the node a name here. OrientDB stores it in the nodeName parameter of OHazelcastPlugin. It adds the variable to your orientdb-server-config.xml configuration file.

Copy the OrientDB folder to other servers that going to be in the same cluster. 
1. Open the config folder and edit  `orientdb-server-config.xml`  
1. Find      <handler class="com.orientechnologies.orient.server.hazelcast.OHazelcastPlugin"> header and in this header find First node name and change it 
_Example:_
TA9OrientDB name of the first node , change it to TA9OrientDB1 save the changes, and close the file

#Running Orientdb as service:
open orientdb.service and chage the file as follow 

[Unit]
Description=OrientDB Server
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=orientdb
Group=orientdb
ExecStart=/opt/orientdb/bin/dserver.sh

copy this file into /etc/systemd/system 
run:
sudo systemctl daemon-reload
sudo systemctl start orientdb
sudo systemctl enable orientdb
sudo systemctl status orientdb

Chech that the service is up. for make sure that the cluster works create new vertex in first server and after that check if the new vertex exists on the second server. 







