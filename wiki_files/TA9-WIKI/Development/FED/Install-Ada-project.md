### Prerequisites:
We are currently running node version `14.21.1` and npm version `6.14.14`. These are the versions you should be running for the projects to run.

1. Clone the DEV_Ada repo. DEV_Ada is located here https://bitbucket.org/ta-9/workspace/projects/FE. 

2. Copy nginx to your machine. Nginx is located in  Work Share (\\10.100.102.13\Nginx). If you don't have access to the share - talk to @<E608786B-5654-64E9-8F2D-46619DC22553> or @<87EAF771-363A-639E-9DA6-BB465A00D649> 
Run nginx. Keep it running all the time you want to access our front end.

3. There are three projects that need to be installed

### fe-angular-app: Oldest, Angular.js project.
Run `npm install`, ignore errors, `npm start` (this will run `gulp serve-dev`)

use type script for auto refresh js files
![Screenshot 2023-02-08 190932.png](/.attachments/Screenshot%202023-02-08%20190932-d94468c6-b56a-4895-953e-e4198a101144.png)

### fe-angular-ng: Newer, Angular 12 project.
First you need to auth your npm to allow using our storybook.
Install auth software for npm
`npm install vsts-npm-auth -g`
Then auth
`npm run refreshVSToken` if it's not working run it from ide i
Same credentials as your windows account.
Run `npm install`, `npm start`
By default NG project will look for it's BE on localhost. Unless you are running your own backend, you should edit a file called `config.dev.json` and update ``apiServer`` entry in the config to the following
```  
"apiServer": {
    "authentication": "http://10.100.102.24:5080/AuthenticationService",
    "userManagement": "http://10.100.102.24:5080/UserManagementService"
  },
```

**Our app should be accessible on http://localhost:4444**

### fe-angular-nx: Newest, nx mono repo that includes the storybook library. Not in use right now, need to update commands. 

Run `npm install`
To build the library: ``npm run build-storybook``
To run storybook interface: ``npm run sb``
To run tests: ``npm run test``
**Storybook app will be accessible on http://localhost:666**


Happy coding!