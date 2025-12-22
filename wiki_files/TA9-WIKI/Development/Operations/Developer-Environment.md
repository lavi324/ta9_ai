[[_TOC_]]
#Introduction
If a developer requires an environment to develop or test his code he can quickly and easily crate one thanks to automation created for this purpose. when you'll find yourself in need of an older version of the code and the database or perhaps one of the many 3rd party application don't seem to work the easiest way to recreate a working environment is using this automation. 

# Requirements
* Access to a virtual machine, one located on your laptop or on an other machine.
* For a local Linux VM - Windows 10 professional.
* Permissions to access Azure Pipelines and the privileges to run builds using Azure git.  

# Instructions 
## Enabling Hyper-Visor
Only for local VM.
1. Ensure that hardware virtualization support is turned on in the BIOS settings.
<IMG src="https://msdnshared.blob.core.windows.net/media/TNBlogsFS/prod.evol.blogs.technet.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/48/12/6116.HVW8a.jpg" alt=" "/>
2. Now we will need to enable Hyper-Visor support for windows 10, to do so click the search icon (magnified glass) on the taskbar or press "Start" and type "turn windows features on or off" then select that item.
3. Select and enable Hyper-V, if required restart your machine.
![image.png](/.attachments/image-86d8c0e4-c221-4fcb-8dbb-ee4761ca01d8.png)
4. After the reboot press start and type Hyper-V Manager to open it.
5. Select Virtual Switch Manager in the Actions pane.
![image.png](/.attachments/image-96696ee2-7012-4905-abb0-b8dbda54cd7e.png)
6. Create a new external switch - ensure that External is highlighted, and then click on the Create Virtual Switch button.
7. Now we will import the Hyper Visor Centos image and create the VM. Press "Import Virtual Machine" and select this folder "\\ta9\share\Artifactory\OsImages\Hyper-V\WE_CentosDev". - This machine will run MySQL, SolR, Orient, WildFly, SeaWeed as dockers
and the Indexing service as a Linux service.
8. Press next until you see the "Choose the type of import to perform" choose "Restore" and continue until the end of the process.
9. Define static IP for you new Linux VM - after the VM starts double click on its name in the hyper visor manager to open its remote Connecticut.
10. Login using the ta9 user password.
11. Go to -> Applications -> System Tools -> Settings -> Network and press on the Cog icon next to the eth0 connection and continue to the IPv4 tab, there change the address from 10.100.102.205 to the IP address you want.
![image.png](/.attachments/image-fc512eb4-a243-40a9-88d2-5407659e3bab.png)
12. Use "ifconfig" in the terminal to validate your new IP.

## Ansible Controller Config
[Ansible in TA9](/TA9-WIKI/3rd-Party-Software/Ansible)
To enable communication between the Ansible controller and the Remote vm we need to copy it's SSH key to the remote machine, to do so:
1. Use putty to connect to the Ansible controller VM.
2. run the following command from console: ssh-copy-id root@TARGET_IP_ADDRESS -f, this will allow Ansible to connect to the remote machine with the user root.

## Running the build
Now we need to Install all required software on our Linux machine, we will use Azure Pipelines for that.
[Azure Pipelines in TA9](/TA9-WIKI/Development/Operations/Builds)
1. Go to [Azure Pipelines](https://ta-9.visualstudio.com/Argus/_build), use your Microsoft TA9 account to login.
2. From the "Ansible" folder select on the "CreateDevMachine" builds and click Queue.
3. Fill the Variables as required and press "Queue". _BranchName is the name of the branch you want to deploy (Do not change what is written under "Branch") _ServiceHost is the IP of the machine that will run Argus Services, _TargetIP is the IP of the Linux VM.
![image.png](/.attachments/image-c6e71a32-ed75-43bc-a33c-0e75d894ead8.png)
4. While you are waiting for the build to finish change the connection string of Argus .net application in the ConnectionsManager.config to fit the MySQL server installed on the Linux VM.
5. When the build finishes successfully the new environment should be working, and ready for development or testing - use any web server just don't forget to change apiAddress of app.config.js in the Login web application.

Enjoy.
