Prerequisites
-
Three servers running Ubuntu 18.04.
A root password is configured on the server.

Getting Started
-
Before starting, you will need to update your system packages to the latest version. You can update them using the following command:
`apt-get update -y`

Install MariaDB Server
-
First, you will need to install the MariaDB server on all nodes. You can install it by running the following command:

`apt-get install mariadb-server -y`

Next, you will need to secure the MariaDB installation and set a MariaDB root password on each node. You can do it with the following command:


```
Enter current password for root (enter for none): 
Switch to unix_socket authentication [Y/n] n
Change the root password? [Y/n] Y
New password:
Re-enter new password:
Remove anonymous users? [Y/n] Y
Disallow root login remotely? [Y/n] Y
Remove test database and access to it? [Y/n] Y
Reload privilege tables now? [Y/n] Y
```


Configure Galera Cluster
-

Next, you will need to create a Galera configuration file on each node so that each node can communicate with each other.

`nano /etc/mysql/conf.d/galera.cnf`

Add the following lines:


```
[mysqld]
binlog_format=ROW
default-storage-engine=innodb
innodb_autoinc_lock_mode=2
bind-address=0.0.0.0

# Galera Provider Configuration
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so

# Galera Cluster Configuration
wsrep_cluster_name="galera_cluster"
wsrep_cluster_address="gcomm://node1-ip-address,node2-ip-address,node3-ip-address"

# Galera Synchronization Configuration
wsrep_sst_method=rsync

# Galera Node Configuration
wsrep_node_address="node1-ip-address"
wsrep_node_name="node1"
```
Save and close the file when you are finished.
On the second node, create a galera.cnf file using the following command:

`nano /etc/mysql/conf.d/galera.cnf`


```
[mysqld]
binlog_format=ROW
default-storage-engine=innodb
innodb_autoinc_lock_mode=2
bind-address=0.0.0.0

# Galera Provider Configuration
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so

# Galera Cluster Configuration
wsrep_cluster_name="galera_cluster"
wsrep_cluster_address="gcomm://node1-ip-address,node2-ip-address,node3-ip-address"

# Galera Synchronization Configuration
wsrep_sst_method=rsync

# Galera Node Configuration
wsrep_node_address="node2-ip-address"
wsrep_node_name="node2"
```
Save and close the file when you are finished.

On the third node, create a galera.cnf file using the following command:

`nano /etc/mysql/conf.d/galera.cnf`



```
[mysqld]
binlog_format=ROW
default-storage-engine=innodb
innodb_autoinc_lock_mode=2
bind-address=0.0.0.0

# Galera Provider Configuration
wsrep_on=ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so

# Galera Cluster Configuration
wsrep_cluster_name="galera_cluster"
wsrep_cluster_address="gcomm://node1-ip-address,node2-ip-address,node3-ip-address"

# Galera Synchronization Configuration
wsrep_sst_method=rsync

# Galera Node Configuration
wsrep_node_address="node3-ip-address"
wsrep_node_name="node3"
```

Initialize the Galera Cluster
-

At this point, all nodes are configured to communicate with each other.

Next, you will need to stop the MariaDB service on all nodes. You can run the following command to stop the MariaDB service:

`systemctl stop mariadb`

On the first node, initialize the MariaDB Galera cluster with the following command:
`galera_new_cluster`

Now, check the status of the cluster with the following command:

`mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size'"`

On the second node, start the MariaDB service with the following command:

`systemctl start mariadb`
Next, check the status of the MariaDB Galera cluster with the following command:

`mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size'"`

You should see the following output:


```
+--------------------+-------+
| Variable_name      | Value |
+--------------------+-------+
| wsrep_cluster_size | 2     |
+--------------------+-------+
```
On the third node, start the MariaDB service with the following command:

`systemctl start mariadb`
Next, check the status of the MariaDB Galera cluster with the following command:

`mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size'"`
You should see the following output:


```
+--------------------+-------+
| Variable_name      | Value |
+--------------------+-------+
| wsrep_cluster_size | 3     |
+--------------------+-------+
```

At this point, the MariaDB Galera cluster is initialized. You can now proceed to the next step.


Disable Case Sensitive
-
In each node edit 50-server.cnf file 

 `sudo vim /etc/mysql/mariadb.conf.d/50-server.cnf`

 Add the next row under [Mysqld]:
`lower_case_table_names=1`

Connect to DB From other Hosts
-
Go again to 50-server.cnf and change binding to 0.0.0.0
save the changes.

Open mysql from the server 
`mysql -u root -p`
run next commands:


```
CREATE USER 'root'@'%' IDENTIFIED BY 'mysql!@#$';
GRANT ALL PRIVILEGES ON * . * TO 'root'@'%';
FLUSH PRIVILEGES;
```
Try to connect to the Database from workbench

Connection String
-
The dotnet framework doesn't supports multiple connections. The connection string is the same as in MySQL.
Dotnet Core Driver supports multiple hosts and the connection string 
e.g
`Server=host1, host2, host3;Database=myDataBase; Uid=myUsername;Pwd=myPassword;`






















