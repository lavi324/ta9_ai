You need to edit [this](https://dev.azure.com/ta-9/_git/Argus?path=%2FWeb%2FTA9.NG%2Fsrc%2Fassets%2Fconfig%2Fconfig.dev.json&version=GBdev&_a=contents) file in our project.
`{
  "env": {
    "name": "DEV",
    "isActiveDirectory": false
  },
  "apiServer": {
    "authentication": "http://10.100.102.220/api/AuthenticationService"
  },
  "defaultDomain": "",
  "appBaseUrl": "http://localhost:4444/",
  "appVersion": "%VERSION%"
}
`

Authorization: The endpoint of the authorization service in the wanted environment.
AppBaseUrl: The URL to navigate to after login.
defaultDomain: For active directory environment.

