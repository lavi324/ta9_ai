[[_TOC_]]

# Installing Java

`yum install `java-1.8.0-openjdk.x86_64`

`sudo java -version`

Output: 
![image.png](/.attachments/image-f47c2859-6209-4161-bbd5-ec1dafaa8fea.png)

#Download And Installing Apache Solr

`wget http://archive.apache.org/dist/lucene/solr/6.1.0/solr-6.1.0.tgz`

##Once the download is completed, extract the service installation file with the following command:

`tar xzf solr-6.1.0.tgz solr-6.1.0/bin/install_solr_service.sh --strip-components=2`


Install Solr as a service by running the following command:

`sudo bash ./install_solr_service.sh solr-6.1.0.tgz -f -i /mnt/app/ -d /mnt/data/ -u solr -s solr -p 9500`

![image.png](/.attachments/image-7a29d30b-feab-4393-a53c-be43bd7ce9f9.png)


# Open the required port:

`sudo firewall-cmd --zone=public --add-port=9500/tcp --permanent`
`sudo firewall-cmd --reload`

## Copy the solr data from working server.

Change pointers to point the new location of the database:


```
/mnt/app/solr/server/solr/freetextindex
					/conf
				             SolrConfig.xml 	--> dataDir should point to /mnt/data/data/freetextindex/data
/mnt/app/solr/server/solr/datamodels
				    /conf
					     SolrConfig.xml 	--> dataDir should point to /mnt/data/data/datamodels/data
/mnt/data/data/freetextindex
							/data
							
/mnt/data/data/datamodels
							/data
```

## Change folder owenership

chown -R solr:solr .* /mnt/data/data/freetextindex/data 
chown -R solr:solr .* /mnt/data/data/datamodels/data)

## Customise 
`vi /etc/default/solr.in.sh` - configure to your needs (paths+memory)

## Common Commands:
You can start|stop|restart the Solr service with the following commands
`sudo service solr start`
`sudo service solr stop`
`sudo service solr restart`









