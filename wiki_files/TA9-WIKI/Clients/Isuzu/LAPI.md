[[_TOC_]]


# Description

The LAPI is a DM, this DM contains info about any traffic violations that happened and it contains info about the vehicle that committed the violation like: an image of the vehicle, car plate, location where the violation was committed, if a passenger was in the vehicle etc. 

![image.png](/.attachments/image-c30c783c-bbff-4955-8d90-40df9ea0ad18.png)

# Autoloader

The data is loading to the data models with auto loader.

| Environments | 'Auto loader path' path | 
|--|--|
| Isuzu Prod + STG |\\\dicdrsrv01\Outgoing\AutomaticJobs\LAPI
|50|/opt/wildfly/upload/lapi


**Wiki on Auto Loader** : [Auto-Loader](/TA9-WIKI/IntSight-Applications/Auto%2DLoader-3.x)

# Parser

The autoloader uses the parser "Traffic Violations" which know to handle the issue of the separated time and date columns in LAPI Data Model.

![image.png](/.attachments/image-2ae06bbb-8a99-4177-a09b-ff58ccc7ecf7.png)


# Custom path

There is a custom path that is defined to divide the image of the violation into 3 different names so that the system can draw only the image that it needs, it divides the name into year, month and day, each of the 3 have their own folder on the server and the system knows the attach the appropriate image to the right violation.

To watch the custom path you can go to MySQL Workbench and type this command:
`SELECT * FROM sqlite_metadata.system_config where ConfigKey='customPathsDefinitions';`

![image.png](/.attachments/image-80cba28a-7c42-4f4e-a816-e29a0afccb17.png)

right click on ConfigValue and click 'Open Value in Editor'.

![image.png](/.attachments/image-29230ecf-4271-4674-90fe-4dfc1a261b88.png)
 



 
**Base URL** : http://intc2/images/lapi/

This URL actually leads to \\\DIFILER01\Lapi\TA9\iis-images\lapi\YYYY\MM\DD and inside the last folder there are images that belong to traffic violations that were committed in the exact day.

**Wiki on custom path** : [Custom-Path](/TA9-WIKI/IntSight-Applications/Field-as-a-CustomPathView)


**The Loading Process**

Once the data has been scanned, the user should drop the photos into the path located on the server: \\\dicdrsrv01\Outgoing\AutomaticJobs\Lapisource

**Note that The folder name must include the date in the following format : ‘yyyymmdd...’ 
For example ‘**20210428**366469’folder name refers to:
2021=year 
04=Month 
28=Day
the photo will move to the path: \\\DIFILER01\Lapi\TA9\iis-images\lapi\YYYY\MM\DD
for example: \\\DIFILER01\Lapi\TA9\iis-images\lapi\2021\04\28
 Successful Data files loaded will be moved to the folder “S” in the Autoloader. The Loading process detailed in this flow schema:

![image.png](/.attachments/image-6e46aa8b-7e18-40fa-8d04-2ac863f8e28b.png)

