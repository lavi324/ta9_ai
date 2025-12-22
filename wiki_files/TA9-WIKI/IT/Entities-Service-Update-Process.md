##steps

1. Undeploy the Entities Service by deleting the EntitiesServices.war.deployed file
2. Make a backup of the EntitiesServices.war file (cp the file to the same directory) in the deployments folder, usually under "%WildFly Folder%/standalone/deployments"
3. Delete the EntitiesServices.war file
4. Open the new EntitiesServices.war using 7-zip or winRAR to view the files inside
5. Take the configuration files out of the EntitiesServices.war file:
app.properties, Application.properties, rabbit_mq.props and Service_2_service.props
app.properties - under \WEB-INF when you open the .war file
rabbit_mq.props and Service_2_service.props - under \WEB-INF\lib\Utils-0.0.1-B31403.jar when you open the .war file
Application.properties - \under WEB-INF\classes when you open the .war file
6. Transfer the new EntitiesServices.war file to the deployments folder
7. make sure the app.properties, Application.properties, rabbit_mq.props and Service_2_service.props are configured well to your environment according to step 8 and transfer them to the Configuration folder, usually under "%WildFly Folder%/standalone/Configuration"
8. 
	A. app.properties -
		I. change the url to the app server url 
	B. Application.properties, rabbit_mq.props -
		I. change to rabbit url – where rabbit installed 
		II. username and password – default guest guest (Encrypted) 
	C. Service_2_service.props 
		I. Change Authenticationurl – app server url 
		II. Change Validatetolen - app server url 
		III. ServiceUser – username: serviceadmin (encrypted) 
		IV. ServicePassword – password serviceadmin password (encrypted twice) 
9. Redeploy the Entities Service By deleting the EntitiesServices.war.undeployed file
10. Make sure after 1 minute that you have a EntitiesServices.war.deployed file