[[_TOC_]]
#Update .env file
To start you need to update the .env file that is located with the docker compose file with the new tag version.
path example: `/root/Documents/swarm/web`
![image.png](/.attachments/image-95996483-47da-425d-849b-fb4bb2efdbc3.png)

#Run the deploy.sh
To run the deploy.sh script use the following syntax:
`./deploy.sh -f web`

![Screenshot_1.png](/.attachments/Screenshot_1-9a9dfe8d-f5c5-40aa-a93a-1a9decfc3f5f.png)

the flag -f is used for what folder to use to deploy the stack, for instance you can deploy backend using -f backend.
