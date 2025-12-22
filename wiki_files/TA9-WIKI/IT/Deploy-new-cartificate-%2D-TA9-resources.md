[[_TOC_]]

# Introduction

There are several resources that we are using in the SSL configuration. 

# TA9 Site List

## https://leappblue.t-a9.com/
## https://leappgreen.t-a9.com/
## https://sense-staging.t-a9.com/
## https://eu-demo5.t-a9.com/
## https://vpn.t-a9.com/
## https://t-a9.com/


All this sites are published with a 3rd party provider.

**The renewal is each year!**

# How to renew in IIS ?
## 1. Look for 5 files:
1. USERTrustRSAAAACA.crt
2. STAR_t-a9_com.crt
3. SectigoRSADomainValidationSecureServerCA.crt
4. AAACertificateServices.crt
5. ccp2020.pfx

**.crt** represents the Certificate itself, it is encrypted.
**.pfx** represent the encrypted file key of the .crt frankly comes together you need to provide it while uploading the crt file.

**make sure you are holding all file in the same directory.**

## 2. Upload the certificate on Windows server

1. Open mmc.
2. File > Add/Remove Snap-in...
3. Select Certificate and move it to selected snap-ins > computer Account> Local computer
![image.png](/.attachments/image-6eb2f0e2-c5fa-4dc6-9359-6c5fc82bf94f.png)
4. Right-Click> All tasks> Import > Choose the file *.pfx file
5. The import will Success.
6. Apply the new certificate in IIS > Open `inetmgr`> Right-Click on TA9 Website> Edit Bindings> Choose an edit :
![image.png](/.attachments/image-c9137768-2593-4b42-a876-ef82dd01cddc.png)
7. Pick the new certificate
![image.png](/.attachments/image-a50ac02f-4839-4167-b4b5-cc363dcf3eeb.png)
8. Validate the new certificate by accessing the site.


# How to renew in cPanel?

1. Access the : https://account.godaddy.com/
2. Login as Admin
![image.png](/.attachments/image-5508e7a2-5a96-4b45-997b-37477950c7be.png)
3. click Manage All
![image.png](/.attachments/image-16480762-a55c-4cf5-83fa-6ac97e1e57cf.png)
![image.png](/.attachments/image-ea114233-c16c-439b-bc6d-23700c8615f6.png)
4. browse to the IP Address.
5. Login as admin
6. Navigate to SSL/TLS
7. On Linux machine you need to get the privet key' but not encrypted.
`openssl pkcs12 -in filename.pfx -nocerts -nodes -out key.pem`
This commans will extract your privet key
8. Upload the STAR.t-a9.com + privetKey you just created.
9 CABUNDLE will generate, keep it in a file, you will need it for VPN setup.
10. Update t-a9 site with the new cartificate.
11. Make sure all setting applied by acceding https://t-a9.com.

# How to renew in OpenVPN?

1. https://vpn.t-a9.com/admin
![image.png](/.attachments/image-3de76ab2-04ca-485d-a7bf-de075d373822.png)

2. Upload all relevant files with Privet Key, CRT, CABundle.
3. Update the server.
4. check settings by accessing 



 
 

