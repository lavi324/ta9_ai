What is in the server:
1. Orient DB - D:\oreint_2.2.37
2. Data - G:\databases
3. Logs on E drive

Windows Services:
1. TA9 OrientDb GraphEd

IIS:
1. Used for getting SSL requests
2. Url Rewrite - [IIS Reverse proxy](/TA9-WIKI/3rd-Party-Software/Servers/IIS/IIS-Reverse-proxy)

Remarks:
When trying to restart the OrientDB window service it may stuck and need to kill the OrientDBGraph.exe from the task manager and then start the service.