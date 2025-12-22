[[_TOC_]]


# There are 3 data models:

1.Hora Data - Data about people that visit in hotels.

2.Hora approval - Data about approvals of the passports of the people by receptionist in the hotel.

3.Hora(View) - view table with data about the people and their passport approval.
 
![image.png](/.attachments/image-19544436-b80e-45a1-bf3d-596e297acf6f.png)

# Autoloader:

The data is loading to the data models with auto loader.

| Environments | 'Hora Data' path | 'Hora Approval' path |
|--|--|--|
| Isuzu Prod + STG |\\dicdrsrv01\Outgoing\AutomaticJobs\HORA\registrations  |\\dicdrsrv01\Outgoing\AutomaticJobs\HORA\validations  |
| Archive | D:\TA9\upload\Registration | D:\TA9\upload\validation |
|50|/opt/upload/Hora|/opt/upload/Hora_approval|


**Wiki on Auto Loader** : [Auto-Loader](/TA9-WIKI/IntSight-Applications/Auto%2DLoader-3.x)

# Custom path

There are five images that exist in the DM's and should be defined in the custom path.

**'Hora data' DM** - Documentimagefilename , Selfieimagefilename , Signatureimagefilename.

**'Hora' view DM** - Signatureimagefilename, Documentimagefilename .

Go to system config table and search for customPathsDefinitions.
right click and click on 'Open value in editor'.

`SELECT * FROM sqlite_metadata.system_config;`
 
![image.png](/.attachments/image-80cba28a-7c42-4f4e-a816-e29a0afccb17.png)

![image.png](/.attachments/image-4d5f00a6-e68c-4a4f-be36-746944323060.png)
 
**Base URL** : http://intc2/images/Hora/

**Wiki on custom path** : [Field as a CustomPathView](/TA9-WIKI/IntSight-Applications/Field-as-a-CustomPathView)