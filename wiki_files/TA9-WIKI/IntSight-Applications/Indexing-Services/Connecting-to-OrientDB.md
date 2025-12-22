#HTTPS
Create the service with the following lines in order to connect to OrientDB

```
set "JAVA_OPS=%JAVA_OPS% -Dclient.ssl.enabled=true"
set "JAVA_OPS=%JAVA_OPS% -Dclient.ssl.keyStore=PATH_TO_KEY_STORE"
set "JAVA_OPS=%JAVA_OPS% -Dclient.ssl.keyStorePass=KEY_STORE_PASS"
set "JAVA_OPS=%JAVA_OPS% -Dclient.ssl.trustStore=PATH_TO_TRUST_STORE"
set "JAVA_OPS=%JAVA_OPS% -Dclient.ssl.trustStorePass=TRUST_STORE_PASS"

:JAVA_OPT_SET

set installCmd="%fullNssmPath%" install "TA9 Indexing Service" "%JAVA_HOME%\bin\java.exe" %JAVA_OPS% -jar indexing.jar
```

and add any other ".cer" certificates to the java environment store using: [Establish an SSL HTTPS connection using non public certificate](/TA9-WIKI/Development/HTTPS-Configuration/Establish-an-SSL%2DHTTPS-connection-using-non%2Dpublic-certificate)
