# Add security headers in IIS manager

1. In the connections pane, expand the node for the server.

![image.png](/.attachments/image-e73a63b0-6069-406e-9876-d091a8a675d8.png)

2. In the site pane, under IIS, double-click HTTP Response Headers.

![image.png](/.attachments/image-98b6da75-5bf5-4d01-8fe7-3e501f106acc.png)

3. In the Actions pane, click Add to reveal the Add Custom HTTP Header dialog box.


![image.png](/.attachments/image-07880e59-e4c6-4397-876f-31a1fd4c057a.png)

4. In the Name box, type in a header name. For example, Referrer-Policy.

5. In the Value box, type in a header value. For our Referrer-Policy example, enter no-referrer. 

6. Click **OK.**

![image.png](/.attachments/image-0bcf0b26-8347-4b03-96bd-531cb34de4e9.png)

7. Delete the header X-Powered-By if it exists. Choose the header, and click Remove in the Actions section.

8. Restart the server

![image.png](/.attachments/image-4cd16ccb-09a8-45f4-9f88-7e5bd13a33c8.png)



# SECURITY HEADERS  (mandatory!!!)
must add them.


| Name | Value  | Description |
|--|--|--|
|Content-Security-Policy | default-src *; style-src 'self' http://* 'unsafe-inline'; script-src 'self' http://* 'unsafe-inline' 'unsafe-eval'; img-src 'self' http://* data:; | Allows website administrators to control resources the user agent is allowed to load for a given page. With a few exceptions, policies mostly involve specifying server origins and script endpoints. This helps guard against cross-site scripting attacks (XSS). |
| Permissions-Policy | fullscreen=() | Provides a mechanism to allow and deny the use of browser features in its own frame. |
| Referrer-Policy | no-referrer |controls how much referrer information (sent via the Referrer header) should be included with requests.  |
| X-Content-Type-Options | nosniff| A marker used by the server to indicate that the MIME types advertised in the Content-Type headers should not be changed and be followed.  |
| X-Frame-Options | SAMEORIGIN | Used to indicate whether or not a browser should be allowed to render a page in a <iframe>, <iframe>, <embed>, or <object>. |



