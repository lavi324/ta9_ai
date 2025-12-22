[[_TOC_]]

# Introduction

Google chrome version 80+ no longr support in SSO ( iFrame ) 
There is a fix from BriefCam should be placed instead of the content of the BriefCam installation.
If you configured the SSO correctly, you will have a problem with the briefcam that the screen is black.

## 1. Open IIS in BriefCam server.
## 2. Stop IIS BriefCam site.
## 3. Open `C:\inetpub\BriefCam\ProWebClient`
## 4. Replace the whole content with this path :
`\\10.100.102.13\Share\Installs\BriefCam\ProWebClient`
**Note:**
web.config & config.js files shouldn't be overwritten by this copy
If another service uses the folder, copy the content of the folders. 

## 5. Restart IIS site
## 6. Test new setting with SSO.

Possible scenarios:
If the problem still happens:

1- check in the network tab, if there are any errors about files that cannot be found in the ProWebClient folder.
For example, if you have an error on this file, change the id in the file's name.
![image.png](/.attachments/image-9da9d4f3-69e0-41db-81ab-5e99d11a888e.png)

2- Check the cookies settings on the user's chrome- enter chrome settings -> privacy and security -> cookies ->allow all cookies