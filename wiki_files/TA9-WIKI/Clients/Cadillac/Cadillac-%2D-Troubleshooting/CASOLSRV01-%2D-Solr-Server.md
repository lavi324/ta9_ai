[[_TOC_]]

# Introduction

Solr is highly reliable, scalable and fault tolerant, providing distributed indexing, replication and load-balanced querying, automated failover and recovery, centralized configuration and more. Solr powers the search and navigation features of many of the world's largest internet sites.

1. The Free Text Repository is where the index of the system is stored.
1. TA9's IntSight is using Apache Solr as the Free Text Repository.
1. The Free Text Repository supports: search, autocomplete, facet-search, highlighting and much more.
1. The Free Text Repository's management console is available at http://10.100.120.83:9500/solr.


# Troubleshooting

## Federated Search doesn't return result

1. ssh to Solr machine
![image.png](/.attachments/image-cabe6367-5469-4bfe-8328-57d835fe84ed.png)
2. Login as ta9 user with password that provided
3. Restart Solr
`sudo systemctl restart solr`
4. Check status
`sudo systemctl status solr`
(should return as running)
5. Mount all external hard drives
`sudo mount -a`
6. Open Chrome browser
http://10.100.120.83:9500
should see this page:
![image.png](/.attachments/image-254c6d68-f545-4692-bdd6-91e807d92c75.png)

Test if it worked: 
Open TA9 App


|No.| Test | Expected Result |
|--|--|--|
| 1. | Login with Admin user |  |
| 2. | Open Federated Search |  |
| 3. | Run a search on an arbitrary word | Results should be displayed |
| 4. | Open an entity from the results | Entity screen will be opened |
| 5. | Open a document from the results | Doc viewer will present the document |


If something went wrong, please turn to TA9 Support team.


