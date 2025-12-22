# Remote Control Isuzu PC's using TigerVNC Viewer 
In order to see the user's machine as the user sees it  (MSTSC is not enough)

- [ ] Connect Isuzu VPN 
- [ ] Connect TigerVNC Viewer
- [ ] Ask Alice for approval to connect the specific computer
- [ ] Fill in computer name and password

_In case of any problem in the connection process please contact Eyal Or_

## For section number 2 you should download tigerVNC Viewer 
_Taken From https://cloudwrk.com/windows-10-remote-access-with-vnc/_

### DOWNLOAD AND INSTALL FREE, OPEN-SOURCE TIGERVNC 64-BIT
Download 64-bit TigerVNC [tigervnc64-1.9.0.exe](https://bintray.com/tigervnc/stable/download_file?file_path=tigervnc64-1.9.0.exe)

Click "Install anyway" on the App Store not verified confirmation window.
Click “Yes” at the User Account Control windows
Click “Next” at the setup windows.
Accept License to continue.
Click “Next” to accept the default program install path.
Click “Next” to accept the default install group name.
Change service settings as needed and click “Next”.
Click “Install” at the summary window.
The final screen is shown. TigerVNC has been installed.

### TIGERVNC CONFIGURATION
Click “START” > Scroll down to the TigerVNC section > Click “Configure VNC Server”
![image.png](/.attachments/image-1fdf90fe-3fd9-45c8-85da-a0d77095868c.png)

Add Password > Click “Configure” > Type a new password (8+ alpha-numeric characters)
![image.png](/.attachments/image-8e605f53-a34c-44c7-94f9-c269721ad9ea.png)

Connections tab > Disable Java viewer on port 5800
![image.png](/.attachments/image-69a4802f-8b40-4a9e-bbc9-d4380b40f53e.png)

Click OK to save settings.

### ALLOW VNC THROUGH WINDOWS DEFENDER FIREWALL
Click “START” > Type “firewall” > Click “Windows Defender firewall”
Click “Advanced Settings”
![image.png](/.attachments/image-65ee9619-6e45-4085-a07f-02480bc2a307.png)

Right-click “Inbound Rules” > New Rule
![image.png](/.attachments/image-e69268d8-8396-47d8-b4d8-e27ead1d39a0.png)

Select Rule Type – Ports, click “Next”
![image.png](/.attachments/image-1aa0cc6c-24f3-45eb-b0fa-bcd1b6961e69.png)

Port type: TCP, 5900 – 5901, click “Next”
![image.png](/.attachments/image-d2196de3-f06e-40f9-a6e7-194009f18b3b.png)

Allow the connection, click “Next”
![image.png](/.attachments/image-63cf95cb-71c3-4867-89c5-5a7d62f12604.png)

Allow for networks Domain, Private not Public. Click “Next”
![image.png](/.attachments/image-664a6c36-d0f4-4aa6-8119-7854056281d6.png)

Service name “VNC”, click Finish.
![image.png](/.attachments/image-ed3a9213-d275-419a-a035-1a4ccfcd63ce.png)

VNC service is now allowed in the firewall.
![image.png](/.attachments/image-5bc637e6-2de1-4224-bd73-835c8682a926.png)

### START TIGERVNC SERVER
Click “START” > Scroll down to the TigerVNC section > Click “Run VNC Server”
![image.png](/.attachments/image-160fc296-7651-49cb-bbb7-8e11c57152d0.png)

Click “Yes” at User Access Control windows
![image.png](/.attachments/image-70843268-08a7-4336-8072-a32b740c06cf.png)

TigerVNC service prompt will show status.
![image.png](/.attachments/image-c3fb6fd0-5a10-43b3-b10a-81963fcf05eb.png)
