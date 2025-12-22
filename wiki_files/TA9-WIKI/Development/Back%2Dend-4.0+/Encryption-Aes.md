# Encrypt code
Encrypt/decrypt for DataConnectionManager found in TA9.Insight.Infra.JwtAuthentication
There is AesEncryptor class  that include :
String EncryptText(string input , string saltKey) – get text and salt key from the DB return the encrypt text.

![Picture1.png](/.attachments/Picture1-b16b8170-4201-47e4-b73a-a14321cbf9d1.png)

String DecryptText(string input, string saltKey) - get text and salt key from the DB return the decrypt text.
The encription key store in vault .
The other key stiore every single connectionstring/user/password in the DB at DataConnectionManager and the field called SaltKey .

There is an **CryptographyConfig** class in TA9.Insight.Infra.Services.Common .
 
![image.png](/.attachments/image-cc679a60-fbca-4543-9cbb-dc3fb6689839.png)

**EncryptController is in MetaData Service**
 
![image.png](/.attachments/image-ffa90feb-9396-4204-a9f9-a67b3380fc9e.png)

**Encrypt Util**
A console application which get 5 parameters :
1. Connection string for DB.
2. Choose 0/1 for Encrypt/Decrypt.
3. Table Name.
4. Column Name.
5. EncryptionKey from vault.
The uti is in metadata repository.

How to use encrypt if I want to check what I got in db – 
We take the text and SaltKey from db that we want to decrypt than we use - Unicode code converter :
_https://r12a.github.io/app-conversion/
and take what we get in uri code.
 We put the text here – 
 ![image.png](/.attachments/image-09f0c14b-8b2d-4d39-89cc-86275516eaec.png)


And take what we got in uri code and put it in the text parameter .
This converter take off special characters.

![image.png](/.attachments/image-51929581-bd0a-42b0-bfa2-2afea5192305.png) 
 
http://10.100.102.23:1025/api/Encrypt/DecryptAes?text=7S0a1N3mJyG%2B6ag3RNVmZQ%3D%3D&saltkey=56d823f2-423c-11ee-bb7e-02420a000046
![image.png](/.attachments/image-a4f30d0a-dd3d-4d84-bcef-b6ff4d6b2f58.png)

The decrypt text return in data .

Now we can use encypt with the data we returnd and the same saltkey , and we can see that encrypt return encrypt text we have in DB

![image.png](/.attachments/image-35edf663-8040-4698-b500-886e0bffa6be.png)
 








