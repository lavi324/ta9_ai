When trying to establish an SSL/HTTPS connection using a non-public certificate

**Subject**
An issue with establishing a trusted connection over SSL in Artifactory

You may run into the following error message during replication and other tasks:

[ERROR] (o.a.a.r.c.BaseReplicationProducer:97) – Error occurred while performing folder replication for 'XXXX': sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target: sun.security.validator.ValidatorException:
 
**Cause**
The error message indicates that Artifactory could not establish a trusted connection over SSL (you may see this issue if you are using a Self-Signed certificate or a certificate that is issued by an internal Certificate Authority or if your clients (e.g. browser, java) are outdated). The trust is handled by having root and intermediate certificates of your SSL certificate on a trusted keystore. 

**Resolution**
The trusted keystore in JAVA is usually at $JAVA_HOME/lib/security/cacerts and the default password of "cacerts" keystore is "changeit". You can import your root and intermediate certificates by using the steps below (For JAVA, you may also upgrade your JDK to resolve this issue as it comes with newer certificates):

1. Download the non-public certificate by performing the following steps
- Navigate to the required URL
- Click on the lock button and click on 'Certificate'
![image.png](/.attachments/image-4abfaa21-c271-4bec-bae2-891a62bb58f2.png)
- On the 'Details' tab click on 'Copy to file'
![image.png](/.attachments/image-4f5ee3e6-c568-47ca-a5f4-c8ee60273d31.png)
- On the wizard choose CER file and name it as you like, this file will be used in the following steps

2. Identify which JVM that Artifactory runs (JDK/JRE/both)

3. For each JVM import root and intermediate certificates to the trusted root certificate of the JAVA (usually called "cacerts") by using keytool import command. For more information, please visit https://docs.oracle.com/cd/E19830-01/819-4712/ablqw/index.html

For example,

`sudo keytool -importcert -keystore /usr/local/java/jdk1.8.0_60/jre/lib/security/cacerts -storepass changeit -file ~/Downloads/RHEL-cert/root.crt -alias "rhel-root"`

OR for windows, open CMD as admin:

`keytool -importcert -keystore "C:\java\jdk1.8.0_221\jre\lib\security\cacerts" -storepass changeit -file "C:\cert\root.crt" -alias "rhel-root"`

3. Restart Artifactory