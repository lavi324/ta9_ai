[[_TOC_]]

#Introduction
Currently all of our development environment are distributed which means 2 machines:
1. Windows:
   * Web hosting
   * .NET services hosting
2. Centos 7 Linux:
   * WildFly Services Docker
   * MySQL Docker
   * SolR Docker
   * OrientDB Docker
   * SeaWeed Docker
   * Indexer Service
   * Loader Service
#Usage
##Windows
Same as always you can RDP to the machine to restart services or check logs with the event viewer.

##Linux
* Checking logs and configurations:
You can access the machine using SMB for example go to \\10.100.102.21\centos, there you'll see:
![image.png](/.attachments/image-ff9e5716-ca68-492a-92d4-fc0d68de094e.png)
For each container service you can enter its directory to see the logs or change configurations, in Wildfly you can also redeploy java services.
For Indexer and Loader use the following commands from putty:

   ```
   sudo systemctl status indexing -l
   sudo systemctl status loader -l
   ```
   Or, if older logs are needed use:
   ```
   sudo journalctl --unit=indexing -n 100 --no-pager
   sudo journalctl --unit=loader -n 100 --no-pager
   ```

### Restart Loader + indexing
```
sudo systemctl restart indexing
sudo systemctl restart loader
```

## Helpful Docker syntax
* Connect to the container:
  1. SSH into the VM using putty
  1. `docker exec -u root -it CONTAINER_NAME bash`
* Managing container status
  1. SSH into the VM using putty
  1. docker stop/start/restart CONTAINER_NAME 
     * For all containers:
       `docker stop $(docker ps -a -q)`
* Delete all stopped containers:
  `docker system prune --all --force --volumes`
## Helpful Linux Syntax
* Managing Linux services
`sudo systemctl start/stop/restrat/status SERVICE_NAME` 