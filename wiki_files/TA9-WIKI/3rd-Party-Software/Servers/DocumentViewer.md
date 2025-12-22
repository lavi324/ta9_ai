[[_TOC_]]

# Validate Folder + location
You need a folder in IIS called DocumentViewer which has access to the library. 

should look like this : 

![image.png](/.attachments/image-f5ba9b1b-f9cf-4384-b694-9f52a50a0a71.png)

Make sure to take the **latest** version of the document viewer from git.

make sure that index.html file is included server IP ADDRESS and port (or /api, depends on the system configuration)

```
			$http({
				method: 'POST', 
				url: "http://10.100.102.24:6180/DocumentsService/documents/RenderDocumentHtml", 
				headers: {'Token': currentUser.LoginToken},
				data:docuViewareConfig
			})
```

# Validate in MySQL the following:

## 1. Document Viewer application defined and active (StateID = 1)
SELECT * FROM sqlite_metadata.sensors;

you should see that the application list pointing to the same address as the document viewer address,
pay attention to the address and protocol HTTP/S

IPADDRESS **must** be identical to the web client DNS/IP + Port.
**ID must be equal to 4!**

|ID| Name | DisplayNameKey | DescriptionKey | ImageUrl | IconUrl | SensorUrl | AcceleratorUrl | IsSystem | IsInternalUrl | OpenMode |StateID | CreatedBy |
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| 4 | Document Viewer | sensor_name_Document_Viewer | sensor_desc_Document_Viewer | NULL | NULL | http://IPADDRESS/DocumentViewer?url=[Value] | http://IPADDRESS/DocumentViewer?url=[Value] | 1 | 0 | 3 | 1 | 1 |

## 2. Document Viewer application **must** be connected to file identifier (-5)
SELECT * FROM sqlite_metadata.sensors_identifiers where SensorID = 4;

![sensors_identifiers.png](/.attachments/image-b69db8eb-3005-4e77-9009-30d8d9a46e1e.png)

## 3. Document Viewer application permission must be enabled for the user trying to open the document viewer



## 4. Validate system config set to DocuViewareLite

SELECT * FROM sqlite_metadata.system_config;

search for DocumentServiceProvider and make sure it defined to: **DocuViewareLite**

![image.png](/.attachments/image-25945776-1e8e-4c36-9a4d-1fa775e72b6c.png)

# 5. Restart TA9 Service Host














