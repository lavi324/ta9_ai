# Incident Not Coming to App

If there are no incidents displayed on the map, there could be several reasons for this:

1. **Token Expiration**: 
   - When a user hasn't interacted with the system for a certain period, the token expires, causing the app to stop displaying new data. 
   - **Solution**: Re-login and reopen Sitpic to refresh the token.

2. **Certificate Issues**: 
   - All Solr instances have their own SSL certificates. 
   - To access the DataModelSearch service, this container must have these certificates in its trusted root. 
   - By default, all certificates are loaded automatically when the container is created. 
   - **Solution**: Run `update-ca-certificates` to validate that the container contains these certificates. 
   - Alternatively, the certificate may have expired or HTX may have provided new certificates for our project. 
     - In this case, refer to the installation guide's SSL section on how to create a new certificate and copy the new one to the stack folder. 
     - Certificates should be in `.crt` format; otherwise, they cannot be loaded into the trusted root section.

# BFT Map and Layers

For these components, we use the same server, EGIS2 (based on Argis Map service). 

If the BFT or Layers do not appear on the map:

- **Check DataModelSearch Service Logs**:
  - The common issue might be an expired or replaced certificate by HTX. 
  - **Solution**: 
    1. Open one of the layers from a Windows or Mac machine (Jump hosts). 
    2. From the browser, export the certificate and replace it with the old one. 
    3. Restart the container.

- **Second Option**: 
  - The problem might be on the EGIS side, and the API might not exist or could be broken. 
  - **Solution**: STE engineers need to report the issue to HTX and wait for a solution from EGIS.

