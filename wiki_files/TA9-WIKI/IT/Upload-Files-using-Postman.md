If you want to upload files to the system, not from the system itself,
you can use another app which is the POSTMAN app!

Download from here (for free) - 
[https://www.postman.com/downloads/?utm_source=postman-home]()

For Example, If you want to upload the template file of the TELCO dashboard export file,
it is highly recommended you will upload it through the Postman app,
since you wouldn't want the file to be accidentally deleted from the load files manager in the system.

**Solution:**
1. open the postman app
![image.png](/.attachments/image-2d9ccf8b-8c4e-4d8a-a86c-64a590612de8.png)
1. create a new request
 ![image.png](/.attachments/image-5b4ce8cf-decf-441d-a718-346de616de4e.png)
1. choose the 'POST' request
![image.png](/.attachments/image-3b09c381-adce-484e-9786-0cacd95715ba.png)
1. in the 'enter the request URL' section:
    - type the file server's IP of the corresponding environment
    - type the file server's port (9334)
    - type the request's type (submit)
all together - <file_server_IP>:<file_server_port>\<request_type>
for example, to upload a file to the 52 environment: "10.100.102.53:9334\submit"
![image.png](/.attachments/image-501ee2a3-5f17-414e-88ce-9833fb8dd34a.png)
1. In the Body tab -
   - choose 'form-data'
   - key = choose 'File'
   - value = select a file from your computer
![image.png](/.attachments/image-bdcc270e-cc51-4055-8e1b-7c8ae89dc81d.png)
1. In the Headers tab - 
   - key = token
   - value = type the correct token
       - open the web system with the relevant environment
       - open the inspect sidebar (F12) 
       - click on the 'Network' tab > 'Fetch/XHR' > select one request > 'Headers' tab > 'Request Headers' Label > 'Token'
       - copy the Token's value
![image.png](/.attachments/image-d87b14fc-c36d-48e4-9598-106487c6529d.png)
![image.png](/.attachments/image-fca958cb-e9cc-4484-ae5d-4d2d8dad0f97.png)
1. Click on Send 
![image.png](/.attachments/image-ec39319d-79ec-4628-af2f-b5f6407fc355.png)
1. If the file has been uploaded successfully, you should get the uploaded file's data such as fid, file name, and file URL.
![image.png](/.attachments/image-5b550817-4700-4dfe-bc76-a4b7e1f7ae55.png)










