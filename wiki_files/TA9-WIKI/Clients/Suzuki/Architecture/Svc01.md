What is in the server:
1. WildFly - D:\TA9\wildfly
2. Indexing Service - D:\TA9\Index Service
3. Text Analytics folder - D:\TA9\TextAnaltycsProviderFiles
4. Logs are located on E Drive

Windows Services:
1. TA9 WildFly
2. Ta9 Indexing Service

WildFly:
1. 

IIS:
1. Used for getting requests from App01
2. Url Rewrite - [IIS Reverse proxy](/TA9-WIKI/3rd-Party-Software/Servers/IIS/IIS-Reverse-proxy)



Remarks:
When trying to restart the WildFly windows service it may stuck and need to kill the java.exe from the task manager and then start the service.