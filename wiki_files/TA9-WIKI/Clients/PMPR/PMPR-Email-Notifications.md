[[_TOC_]]

#Summary
In PMPR's project they load loads of PSTs. 
We have created a Post Loading Action that will send an email to a user, with access to the specific case, regarding words-of-interest, if they are present in the current loaded PST.

## Add the DLL

Place it on:
"C:\Post Loading Actions"


#How it works
Keyword - the word itself.
Id - An auto-increment id.
CaseNumber - The number of the case we want the word to be related to.

The PLA gets the relevant words to the case, searches for the related case users and sends them an email, if at least one word has been found.

1. Make sure ta9data.email_keywords is present. It looks like this:

![image.png](/.attachments/image-50c23c7e-769c-426b-b793-23993cbeeb72.png)
![image.png](/.attachments/image-fd532516-5f6f-4d96-9ce1-0352acd6cc0d.png)

2. Make sure it is defined on LookupManager:

![image.png](/.attachments/image-e7a572fe-6a75-4d92-835c-ba318a84f666.png)

3. Make sure the users have emails on the table:

![image.png](/.attachments/image-eb96a949-ac3f-4130-87b3-490f89ee7f4c.png)

4. Make sure that case id is connected to the wanted user id:

![image.png](/.attachments/image-377770c6-c56c-4239-9904-fe6c1031f945.png)


Now, just load a PST and wait for the email!

![image.png](/.attachments/image-77eac5f3-6034-4f6f-ab16-dae43ddffdf9.png)

We would also get a mail about successful upload of the file:

![image.png](/.attachments/image-79520723-1bf0-4c58-a446-49bb35b41474.png)

