[[_TOC_]]

# Troubleshooting
In case the face recognition app isn't displaying detections do the following:

1. ssh to the CAANYSRV01 machine.
2. login with maint user (use the provided password)
3. Switch user to:
`su - anyvision`
4. restart containers: 
`docker restart $(docker ps -qa)`
5. Check status: 
`docker ps -qa` 

all containers must to be on running state.

Go back to TA9 system:


|No.| Test | Expected Result |
|--|--|--|
| 1. | Log in with Admin User |  |
| 2. | Open Face Recognition Application |  |
| 3. | Click the "Search" tab | See detections |

*Detections should only arrive at the Face recognition module after uploading a video file with faces to detect, via the application Autoloader.


