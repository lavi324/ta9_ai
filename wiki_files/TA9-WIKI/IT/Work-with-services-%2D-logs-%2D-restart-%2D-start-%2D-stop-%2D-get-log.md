[[_TOC_]]
# Working with Linux services
Different Commands to services:

**Service_Name can be any service that runs on the same machine like solr, orientdb, indexing, loader etc.
1. Restart service:
`systemctl restart *Service_Name*`

2. Status Service:
`systemctl status *Service_Name*`

3. Check for logs and write them down to a folder:
`sudo journalctl --unit=Service_Name -n 100 --no-pager`

The command above will show you the latest 100 lines in the logs of the service you wrote down, to get more logs change the 100 value to higher value.

To write down the logs to a file use the next command:
`sudo journalctl --unit=indexing -n 100 --no-pager >> /*Path_to_service_folder/log.txt*`

You will need to find the service folder or create it locally and find it thorugh the FileZila after you created the file.

#Different commands to Docker:

Check for Status:
`docker ps`

Restart Docker Containter:
`docker restart *Container_Name*`

Execute commands into the container:
`docker exec -it *Container_Name* *command*`

#Working with windows
