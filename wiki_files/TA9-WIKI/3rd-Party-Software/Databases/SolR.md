[[_TOC_]]

#Introduction
Solr is highly reliable, scalable and fault tolerant, providing distributed indexing, replication and load-balanced querying, automated failover and recovery, centralized configuration and more. Solr powers the search and navigation features of many of the world's largest internet sites.

1. The Free Text Repository is where the index of the system is stored.
2. TA9's IntSight is using Apache Solr as the Free Text Repository.
3. The Free Text Repository supports: search, autocomplete, facet-search, highlighting and much more.
4. The Free Text Repository's management console is available at http://solr_server_address:9500/solr.

#Installation
## Windows
1. Copy \\\10.100.102.13\share\Artifactory\Deployment\DBs\solr-6.1.0 locally 
2. Run _CreateTA9SolrService.cmd as Admininstrator.
3. Go to http://solr_server_address:9500/ to validatate installation (make sure the service created in previous step is running).

##Linux
1. You can run a [playbook](https://ta-9.visualstudio.com/Argus/_git/CM?path=%2FAnsible%2FDBs%2FSolR.yml&version=GBmaster) using ansible to deploy a SolR server.
2. If installing manually you can use this guide: [https://devops.ionos.com/tutorials/install-and-configure-apache-solr-on-centos-7/](https://devops.ionos.com/tutorials/install-and-configure-apache-solr-on-centos-7/)

# Help-Full Commands
# #Delete:
To clear all data from a SolR core go to the document page pick XML and paste the following:
`<delete><query>*:*</query></delete>`

## Delete DM:

Goto solr interface & choose create the following command. instead of "item_type:2", type: "resource_name:DM_ID"

![image.png](/.attachments/image-fd027d57-8cce-4f0f-986a-4742bc9927d2.png)

a.	Hit ‘Submit document'







##Commit:
Fore commit by changing the server IP and pasting the following:
`http://localhost:9500/solr/freetextindex/update?commit=true`
* this action is not recommended because it messes the commit timings of the SolR and might create performance issues. 

#Troubleshooting

##The search does not return values
* Go to Solr's management console and see the collections are there and returning values. If not, refer to the 'Logging' page of the console and act according to the error.
e.g. http://solr_server_address:9500/solr/freetextindex/select?indent=on&q=*:*&wt=json should return items

##The search operation takes long time
* When there are many documents in the repository, it takes some time for the Solr index to built. So:
 If the Solr instance was launched lately, wait about 30 minutes and try again.
 If it's not the situation, refer to the 'Logging' page of the console and act according to the error.

##The autocomplete is not working
The autocomplete feature of the [[Free Text Repository]] requires a lot of RAM to be supplied to the Solr than the normal search.
Therefore, in cases when not enough memory is available, the autocomplete feature is not working. A message like this usually appears:
"Lookup is not supported at this time".
This problem can be easily fixed by increasing the memory allocated to the [[Free Text Repository]].
* Use the ''-m'' flag of the service to increase the memory allocated. Eg - ''-m 6g'' will allocate up to 6 GB of RAM to the Solr service.

## Core Service stopped working

Error opening new searcher - Index corruption

Index corruption are generally very rare and might occur because of the following reasons:
1. Power outage - The system was running a "commit" and the server went down because of a power outage.
2. Process was killed while the index was being written to
3. Indexing concurrently into the same index by disabling index locking.

The best approach would be to stop Solr and take a backup of the index.
Once backed up you can try the following command options on the index to:
###Solution 1
1. Try to see if the index is really corrupt
2. Try to debug the cause of index corruption
3. Try to fix the damaged segments else, remove them.
4. Run CheckIndex to verify index
5. Restore the index (some documents will be gone) but hopefully a good part of the index should be recoverable.


_________________________________________________________________________________________

###Solution 2
1. Stop the Solr node

2. Backup the index directory if data is of paramount importance

3. Goto <Path_to_SolrInstall-X.Y.Z>/server/solr-webapp/webapp/WEB-INF/lib

You should see lucene-core-X.Y.Z.jar here:


Run the following command:

Syntax:

`java -cp lucene-core-6.3.0.jar -ea:org.apache.lucene... org.apache.lucene.index.CheckIndex <path_to_index_folder> -exorcise`
 
**Example:**
`java -cp lucene-core-6.3.0.jar -ea:org.apache.lucene... org.apache.lucene.index.CheckIndex /Users/Rohit/Documents/SolrInstall/solr-6.3.0/example/cloud/node1/solr/gettingstarted_shard1_replica1/data/index -exorcise`




## Solr boots & immediately stop
Increase memory allocated for Solr (change -m flag of startup command)
