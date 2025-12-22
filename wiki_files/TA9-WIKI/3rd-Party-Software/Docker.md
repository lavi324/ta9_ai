[[_TOC_]]

# Introduction 

<B style="font-weight:normal"  id="docs-internal-guid-296fd5ef-7fff-9f53-9a3c-536fa206a38e"><SPAN style="border:none;width:602px;height:301px"><IMG  src="https://lh5.googleusercontent.com/AaWhUOxCD0FNsnwoYL_nxj6m6qiyIScTLbrz5t0Gy0mkngU2VdcB8Wlp9fQRiqVEzxo-6nh8EhkvRZRIgsRLY79G4zKqihYVIQDaeshKAz2nBw3y478FJbe0q7qU6wURVL_RhEEd"  width="602"  height="301" style="margin-left:0px;margin-top:0px"/></SPAN></B>

Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.
Containers are isolated from one another and bundle their own software, libraries and configuration files
They can communicate with each other through well-defined channels.
All containers are run by a single operating-system kernel and are thus more lightweight than virtual machines.
The service has both free and premium tiers. The software that hosts the containers is called Docker Engine


# Docker in TA9

## Install Docker via Ansible 

Log on to Ansible controller (10.100.102.19)

`ssh-id-copy ta9@xxx.xxx.xxx.xxx`

After Paswword typing in the machine 

`vim /etc/ansible/hosts`

Add the designated machine

save and exit. 


```
cd ~/test-playbooks

ansible-playbook docker.yml -l XXX.XXX.XXX.XXX
```


We use Docker to implement and run our machine to achieve a faster response from servers.

# Get familiar with our Docker files: 

See which docker files are running:

`docker ps` 

The running machines: 

![image.png](/.attachments/image-8d72c977-8911-4708-8865-6168d62efe6e.png)

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
    Clear Journal:
   ```
   sudo find /run/log/journal -name "*.journal" | xargs sudo rm
   sudo systemctl restart systemd-journald
   ```
# Stop all docker runing machines: 

`docker stop $(docker ps -a -q)`


# Location of the docker 
`~/opt`

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




