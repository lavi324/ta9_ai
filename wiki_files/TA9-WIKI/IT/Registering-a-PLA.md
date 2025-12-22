#Registering a PLA in to the system


### To register a PLA, follow these steps:
#
1. Deploy the PLA image.
2. Open Admin Studio and navigate to > Data Models > Post Loading Actions > New
3. In the PLUGIN CONNECTION popup window, fill in the fields, and choose the relevant Post Loading Action Type- Synchronous or Asynchronous:
4. Test the connection and click ADD PLA

![image.png](/.attachments/image-0121678a-e638-4d5e-ab14-fbaf75c7e878.png)

In the Post Loading Action URL, fill in the following URL according to this template:
#
# http://<traefik_service_name>/<PLA_service_name>/api
#

- ###The Traefic service name can be found by executing _`docker service ls | grep traefik`_, or in Portainer
- ### The PLA name can be found in traefik (IP:9080) > services 
- ### Notice that the PLA name should **not** contain the plugins proxy stack name
### For example:
_http://plugins__proxy_hub/insertupdateevents/api_


