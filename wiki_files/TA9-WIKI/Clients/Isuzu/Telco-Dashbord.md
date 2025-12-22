[[_TOC_]]

#Telco DashBoard

![image.png](/.attachments/image-edf36810-8409-4130-9183-57ab3660754d.png)

Telco Dashboard is a unique dashboard for our client in : ISUZU.
it is customised as the client asked it. 


# Troubelshoot

## Export from Dashboard dosen't working

java.io.FileNotFoundException; http://10.100.102.32:6380/FileServer/files/12,02a5ba9bf898b3?TOKEN=f8ad93d95c5848a99b4d9c3968e12a3f

1. Make sure ReportsGenerationService.war in WildFly is running and deployed.
2 . In MySQL make sure thet you have the template of the file

`SELECT * FROM sqlite_metadata.system_config;`

look for : **DashboardExportTemplate**

 

