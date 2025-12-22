[[_TOC_]]

#Introduction
Microsoft Azure (formerly Windows Azure /ˈæʒər/) is a cloud computing service created by Microsoft for building, testing, deploying, and managing applications and services through Microsoft-managed data centers. It provides software as a service (SaaS), platform as a service (PaaS) and infrastructure as a service (IaaS) and supports many different programming languages, tools and frameworks, including both Microsoft-specific and third-party software and systems.

As for now All of TA9s Demo environments are hosted on Azure and are separated by resource groups.

https://portal.azure.com/#blade/HubsExtension/BrowseResourceGroups

#Resource groups
Each group should contain the following:

![image.png](/.attachments/image-d9898074-1934-4352-aa5b-a95dbca545bb.png)

* The Europe-Demo Resource group has items that are used by several VMs like the network security group.
* The Mazda group has both leapp applicaitons green and blue (mazda VM is blue)
* The PrizmDocument group contains all the items for the Prizm document viewer, it's connected to the network of the EU instance and is used by them.  


