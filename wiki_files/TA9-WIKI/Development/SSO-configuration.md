## 1. Authentication Config in Vault:
_LoginAuth_ should be a number, 1\2\3 according to the Enum - 
![image.png](/.attachments/image-86bc6609-1df8-4361-847d-b21ec40f37c0.png)
![image.png](/.attachments/image-eb2d6818-01bc-450e-bfd2-b10f63e1aa09.png)
## 2. External User Management in Vault:
_DataSource_ should be a number, 1\2\3 according to the Enum - 
![image.png](/.attachments/image-1e4caecd-445f-4c32-b591-af21a7afccdc.png)
![image.png](/.attachments/image-fe2d0484-eb41-404d-9178-a38651b5681c.png)

### This Enum also available in MariaDB - 
`SELECT * FROM sqlite_metadata.usermanagement_datasource;`

![image.png](/.attachments/image-3a135a5c-d5ea-408c-a191-11ac2b81794c.png)
## 3. Authentication SSO in Vault:
_ValidationClaims_ KeyValue properties (_'aud','azp','iss'_) should vary from one client environment to another
![image.png](/.attachments/image-83384942-a87e-4e6c-92ed-e8ab733236bf.png)
## 4. Authentication Service Config:
A config file named '_appsettings_config_sso_test_' attached to the _Authentication_ service under the _Backend_ stack
- _AuthenticationSso_ should be exactly the same in structure as the Authentication SSO object in Vault (section 3)
![image.png](/.attachments/image-5bfa22e1-d08d-40da-bef6-7dd57301bbf4.png)
### It should be attached right here -
![image.png](/.attachments/image-d6bab781-6b3c-4362-bca9-7072f06d5804.png)

![image.png](/.attachments/image-4e274388-9fd6-4964-bde4-136a0379d71f.png)
## 5. Frontend Config:
A config file named '_config_ng_sso_enabled_no_justification_fixed_copy_' attached to the _web_ng_ service under the _web_ stack
- _providerUrl_ should be according to the "iss" property under Authentication SSO in Vault (section 3)
- _clientId_ should be according to the "azp" property under Authentication SSO in Vault (section 3)
![image.png](/.attachments/image-7eb1a8f5-0c79-460f-992a-c361ca2f5258.png)
### It should be attached right here -
![image.png](/.attachments/image-4fd40433-b313-4601-88f6-4590944a0207.png)

![image.png](/.attachments/image-608b974a-9fcb-4fcf-b7f9-26c0e1105db4.png)
### Replace the older Config file attached to this service
![image.png](/.attachments/image-9cff134c-36fd-41fd-a666-afecfb9c373e.png)


# Result:

![image.png](/.attachments/image-1e85020e-84ce-4b03-a865-ecfe5daeff4c.png)

![image.png](/.attachments/image-e7982ab3-d1b0-4c66-9f42-af334b4d4ed4.png)

![image.png](/.attachments/image-02ac2e72-8cab-4d05-b633-55c03e14a0eb.png)

![image.png](/.attachments/image-e86dd747-3a02-484c-a600-0da84db5d305.png)

### To make sure the procedure goes as it should, the usual Login method redirect into the LoginJWT method - 
![image.png](/.attachments/image-9505d31e-9bd4-439d-b879-2a2d800e3df7.png)