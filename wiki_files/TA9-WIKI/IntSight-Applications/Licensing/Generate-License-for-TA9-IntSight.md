#Do not use the application without consulting the IT\Devops!

##Application
To generate new license for a client/dev enviorment please use the **application LicenseGenerator** that located in:

`\\10.100.102.13\Share\Artifactory\TA9Tools\LicenseGenerator`


##GUI

![image.png](/.attachments/image-f409b760-9901-4039-958a-3fc95975999c.png)

1) Client Name - Choose the name of the environment you will be producing the license to.(doesnt affect the real license)
2) Number Of Users - Choose the number of users that will work on the environment.(affect the real license)
3) Expiration Date - Choose the date that the license will end at. (affect the real license)

After you fill up all the above correctly press generate and choose where to save the new license.

2. **Open the license Uploader** (located in: `\\10.100.102.13\Share\Artifactory\TA9Tools\LicenseUploader\LicenseUploader`)

![image.png](/.attachments/image-fef96641-8100-460e-982f-2a7ad2894518.png)

1. DB Host - MySQL DB IP of the environment you will be producing license to.
2. DB User - root
3. DB Password - ...

Finally, select the license file you generated and Upload.

-----
If you will need to apply the new license manually (via DB) please use the guide: https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/479/Activate-TA9-Insight-app-Manual
OR
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/455/Activate-TA9-Intsight-app-Automatic


