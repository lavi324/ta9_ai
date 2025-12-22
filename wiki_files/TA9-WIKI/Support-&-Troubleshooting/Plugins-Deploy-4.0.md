1. login to docker hub
2. Go to filezilla and go to /opt/plugins to edit docker-compose.yml
2.1 for new plugin:
paste the new service pattern (without the seperators)
-----------------------------------------------------------------------
calltypeplugin:
    image: ta9repo/ta9.isuzu.plugin.calltype:4.0.0-1
    ports:
      - 10102:80
    configs:
      - source: odbcini
        target: /etc/odbc.ini
      - source: phoneconfig
        target: /app/PhoneDashboardConfiguration.json
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
(Here, Development environment is set because this helps us test the containers locally. If it does not set to this parmeter, Swagger would not be enabled and we could not test it locally.
-----------------------------------------------------------------------
a. Edit the container name - change it to the service name + plugin (marked in yellow)
b. Edit the image name ta9repo/$FULLIMAGENAME$:$IMAGEVERSION$, as it is written in the docker hub (marked in pink)
c. Edit the port, just go +1 on the last you can see and check with Ctrl+F that the port is not used in the file (marked in orange)
d. After you made sure all the setting are configured right and you finished with all the plugins, go to /opt/plugins in the server that is supposed to run the stack and run the command:
docker stack deploy --with-registry-auth -c docker-compose.yml %STACKNAME%
e. Make sure on portainer that the stack is up and services are running
f. Make sure docker compose file has relevant "network" configuration, like "bind" or "volume" (this should be DevOps responsibility but you need to make sure this section exist, otherwise the plugin/parser would not get any incoming requests.

2.2 To update a plugin

a. Go to portainer, go to the stack your service runs in, delete the service you are updating
b. Go to Docker hub, go to the ta9 repository and go to the service you need to update
c. Make sure that docker-compose.yml contains the right container name (marked in yellow), right service name (marked in pink)
d. Update the version number on docker-compose.yml to the newest version that is mentioned in the Docker hub
e. After all services have been updated, go to /opt/plugins in the server that is supposed to run the stack and run the command:
docker stack deploy --with-registry-auth -c docker-compose.yml %STACKNAME%
