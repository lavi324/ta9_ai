 

# SSO Support 

 As part of the 4.2 version, we offer our support in SSO integration when logging into TA9 IntSight. The Login into the system is via a 3-party authenticator that redirects back to the portal. The entire authentication process is managed outside of TA9. 

![image.png](/.attachments/image-2fafd98d-b1be-4ced-b5a2-3cf8f74220d4.png)

This feature is presented on the first page of TA9. The login button leads the user to the Portal page, where can click “login” to initiate the authentication process, which eventually results in a token, which will be sent back to TA9 allowing the login.  

![image.png](/.attachments/image-f39c3eb3-044b-4aba-8c1e-95fca0484986.png)


# SSO Diagram 

TA9 supports OpenID implicit flow Single Sign On for authenticating users. 

The following chart represents the flow of the process: 

![image.png](/.attachments/image-bc7a9fbd-c2dc-4199-ab50-8a6438a3ff8f.png)


# Client to provide. 

 When integrating with SSO, each project has its guidelines, including: 

## URL for redirecting: 

The URL for inserting the user’s credentials for authentication. 

## Token Validation flow: 

- The Validation process of the token TA9 receives - Test specific properties/ Certificates/ External URLs. 

- A token sample. 

## The claims that contain the login name of the user: 

The list of claims we can extract the Login name from the token. 