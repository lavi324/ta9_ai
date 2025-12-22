[[_TOC_]]
## Intro
A build that's taking all base images from the following directory:
\\10.100.102.13\Share\Artifactory\BuildFiles\FileServerImages

On that folder, it searches for sub folders named as table names and each file is named as the ID of the corresponding table.

The build is doing the job by reading the contents of the folder, upload the files to the FileServer and update the DB with the new file-id's.

## Parameters
Some parameters must be provided before running the build:
1. MySQL_IP - IP/Host of the DB
1. MySQL_User - DB user
1. MySQL_Pass - DB user's pass
1. SeaweedFS_IP_HOST - IP (or hostname) of the file-server

## Sample
![image.png](/.attachments/image-9226b616-f8c7-4f2a-abb1-919e249fb4fb.png)