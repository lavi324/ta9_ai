# Ansible

![image.png](/.attachments/image-ceae1e0e-e9be-4087-a293-6019c9108582.png)


Ansible is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

[Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)

## Key-Words
* Controller - The Ansible agent that responsible for invoking commands on remote machines, the main Ansible application which contains the configuration and the hosts file. 
* Hosts file - contains the list of remote machine divided by groups (/etc/ansible/hosts).
* Playbook - A script of sorts written in YML contains the commands that will run on a remote machine [Playbook Repository](https://ta-9.visualstudio.com/Argus/_git/CM) 

## Local implementation
Currently Ansible is installed on 10.100.102.19 and is used to quickly create a working environment for developers.
In the future it will be the main tool to manage the different configuration to each machine.   
