As part of the 3.9.3 version, we offered our support in SSO verification when logging into the app.

During the login flow, we receive a token to be later validated using an API URL.

The verification is done with the following prerequisites and in the following flow. 

- The user will have a record in the **Users** MySQL table, where the login name is the ID of the DRI user. 

- The folloiwing Configuration shuold be inserted.

**C:\Program Files\TA9\Web\NG\assets\config\config.deploy.json**
* See the following example section that should be inserted into this config: 

   "sso": { 
	"enable" : true,
	"tokenPrefix": "Bearer",
	"clientId": "ipolice-police-belgium-eu",
	"scope": "openid",
	"providerUrl": "http://localhost:9091/common/oauth2/v2.0/authorize",
	"redirectUrl": "http://sd-fcsi-wb01788.bpolb.eu/ng/login",
	"responseMode": "fragment"
	},

**C:\Program Files\TA9\C#\TA9 Core Services\Services\Authentication.Service\Authentication.Service.dll.config**
- See the following example section that should be inserted into this config:
  <appSettings>
	<add key="SSO" value="true"/>
	<add key="ValidationUrl" value="https://services.pol.be/toser/Api/v2/ValidateToken.php"/>
	<add key="ValidationMode" value="DEV"/>
	<add key="ClientId" value="ipolice-police-belgium-eu"/>
	<add key="Audience" value="pol.be"/>
	<add key="Issuer" value="pol.be"/>
  </appSettings>