[[_TOC_]]
#Inroduction
Some of the most used builds
# STG_Full_Build_DIS
Very much like the regular gen build but used with distributed environment of 2 machines.
**All current development environment should be updated using this build**.
* running the build you must input some variables:
![image.png](/.attachments/image-8b443ada-8888-446c-88fc-eda560103b37.png)
   * _LinuxHost - Linux host ip
   * targetIp - Windows host ip
   * Don't forget the correct branch. 

This build compiles and deploys all projects, that means if an older branch is being used the build can be partially successful because it might miss the NG application.


#CreateDevMachine
A Build that creates a full dev environment on a personal computer.
Full guide:
[Developer Environment](/TA9-WIKI/Development/Operations/Developer-Environment)

# Development Machines and Initialize Development Machines
A Build that creates a full dev environment on two VMs.
* Development Machines is for configuration updates
* Initialize Development Machines is for creating new environmets - if used on an existing instance the instance will be reset.

##Requirements
2 empty VMS
* Linux - \\\10.100.102.13\share\Artifactory\OsImages\VMware\TM_CentosGen image can be used, you can use [Developer Environment](/TA9-WIKI/Development/Operations/Developer-Environment) to configure this VM

   * Set a static IP
   * Add This Line to Centos :
   `echo "TA9 ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/TA9`

cd /etc 
vim fstab
**Add this lines:**

```
/dev/mapper/centos-swap swap                    swap    defaults        0 0
//10.100.102.13/share   /mnt/smb/               cifs    username=guest,password=,file_mode=0777,dir_mode=0777,vers=2.0  0  0
```

Restart the VM
_______________________
* Windows - \\\10.100.102.13\share\Artifactory\OsImages\VMware\WE_DEV_WIN image can be used
   * Set a static IP
   * run the following from an elavated powersehll console: 

   ```
   $url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
   $file = "$env:temp\ConfigureRemotingForAnsible.ps1"
   (New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
   powershell.exe -ExecutionPolicy ByPass -File $file
   Enable-WSManCredSSP -Role Server -Force
   ```
* Add the new VMs to the host file on the Ansible controller:
  1. sudo nano /etc/ansible/hosts
  1. 
     ![image.png](/.attachments/image-a0def79d-683c-4f4d-9098-07204d4a838b.png) - Windows Group
     ![image.png](/.attachments/image-b2f119b7-46a4-48ad-a49c-765f270f176e.png) - Linux Group
     [Win-Local-Dev-Servers:vars] - this section contains the credentials for the windows machiens connections
##Running the build
* Now you can run the Initialize Development Machines for a new environment
* Run Development Machines  to update the configuration as written in the Ansible playbook. the configurations will be applied to all the machines in the 2 groups.  

#GEN_Full_Build_Only 
The same as GEN_Full_Build or GEN_Full_Build_DIS but will not deploy the artifacts to an environment, instead it will create an artifact package at \\10.100.102.13\share\Artifactory\Temp\WINDOWS_HOST_IP

* You can use GEN_Full_Build_Only-Librery to create artifacts for specific clients 
![image.png](/.attachments/image-ee2383da-f30c-4824-a71f-fd3c383e2fdc.png)

just pick the correct Variable group before running the build.

* variable groups can be defined here:
![image.png](/.attachments/image-901d1de3-0250-4f70-8cc8-e6931def4264.png)
