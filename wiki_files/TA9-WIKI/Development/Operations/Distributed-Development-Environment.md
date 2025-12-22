[[_TOC_]]

#Introduction
Create a new distributed environment using playbooks.

# Instructions:
1. Create 2 Virtual machines using the following OVAs:
   "\\\10.100.102.13\share\Artifactory\OsImages\VMware\TM_CentosGen"
   "\\\10.100.102.13\share\Artifactory\OsImages\VMware\WE_DEV_WIN"
2. After they are loaded set static IPs to both machines.
3. On the Windows machine run the following script as Administrator from power shell.
   
```
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"
(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file
Enable-WSManCredSSP -Role Server -Force
```
4. From the Ansible controller run the following command:
```
ssh-copy-id root@LINUX_MACHINE_IP -f
```
5. Update the hosts file in the Ansible controller
```
sudo nano /etc/ansible/hosts
``` 
6. Add the Linux machine IP under [Centos-Local-Dev-Servers]
7. Add the Windows machine IP under [Win-Local-Dev-Servers]
8. Use the following build: [Development Machines](https://ta-9.visualstudio.com/Argus/_build?definitionId=107), Set the variables like so:
![image.png](/.attachments/image-7e1b2783-44b1-47f9-b4d4-d8e07f7facbc.png)
9. Run the build and wait.
