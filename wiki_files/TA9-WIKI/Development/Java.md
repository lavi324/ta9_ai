[[_TOC_]]

#Environment installation:
	1. Install eclipse - http://www.eclipse.org/downloads/packages/eclipse-ide-java-ee-developers/oxygen2
	2. Download WildFly - http://download.jboss.org/wildfly/10.0.0.Final/wildfly-10.0.0.Final.zip
		a. Save it to c:\wildfly-10.0.0.Final
		b. Increase max upload file size (C:\wildfly-10.0.0.Final\standalone\configuration\standalone.xml)
		<server name="default-server">
		                <http-listener name="default" max-post-size="999999999" max-header-size="999999999" socket-binding="http" redirect-socket="https"/>
		                <host name="default-host" alias="localhost">
		                    <location name="/" handler="welcome-content"/>
		                    <filter-ref name="server-header"/>
		                    <filter-ref name="x-powered-by-header"/>
		                </host>
		            </server>
		c. Change port from 8080 to 9900 on C:\wildfly-10.0.0.Final\standalone\configuration\standalone.xml
			a. `<socket-binding name="http" port="${jboss.http.port:9900}"/>`		
	3. Download postman chrome extension - https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop
	4. Install Maven - 'http://www.java2blog.com/2015/09/how-to-install-maven-pluginm2eclipse-in.html

#Environment configuration:
	1. Open Eclipse and define c:\argus\java as default workspace
	2. Import projects: File->import->General->Existing Projects into Workspace
	3. Select c:\argus\java as root directory
	4. Select All Projects 
	5. Install Jboss Tools from Help->Eclipse marketplace
	6. Add WildFly 10.0 server using: Window->Preferences->Server->Runtime Environment->
	7. Update project
	8. Change port from 8080 to 9900 on C:\wildfly-10.0.0.Final\standalone\configuration\standalone.xml
		a. <socket-binding name="http" port="${jboss.http.port:9900}"/>
	9. Run server

