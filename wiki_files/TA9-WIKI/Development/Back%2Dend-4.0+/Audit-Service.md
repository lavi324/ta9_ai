**Audit**
Audit Service insert audit information into metadata DB, in the following tables:
- queries_audit
- data_audits
- login_audit

The relevant API's send the relevant info to Audit service using SendToAudit attribute, that analyze the data and transfer it to audit object (like DataAuditItem) and send it to RabbitMQ (submit-audit-events) using Infra.AuditProducer NuGet. 
Services in Java directly activate the API's in the Audit service without using Q message.

![image.png](/.attachments/image-7bc6f3ba-f21e-490d-8a50-20949943a3b8.png)
  
**Audit General Flow :**
![image.png](/.attachments/image-fa988612-d6f4-4d9c-a733-15a17d2e1344.png)

**Audit flow in services :**

**Authentication service** - records every login/logout attempt into login_audit table.
*Any authentication verification failure for token is also logged throw specific middleware extension in Gateway Service. 

![image.png](/.attachments/image-e85a5375-7a82-45ca-ab6f-bf373755fbcd.png)

The following info is saved in the table :

![image.png](/.attachments/image-30842b75-780c-40e3-a01c-bc1683b187a6.png)

**Task service**- this service create scheduled search and records it in queries_audit

![image.png](/.attachments/image-658aff6e-a6a8-42ba-9b0a-d9cad3eb89aa.png)

**Entity Management** in MetaData service - 
![image.png](/.attachments/image-e5947d0d-a3da-4e09-b762-93011cbe3901.png)

records changes in entities. also java service records changes in entities and record it in the following table data_audits :
![image.png](/.attachments/image-9ed619e8-4a26-40b3-bd2c-bcd277b3f94c.png)

**DataModel Search service**

![image.png](/.attachments/image-ac769200-ef3d-4db9-ba87-26c23c54457b.png)

**Case Management Service** - 

**Java Service (Entities, Federated) Service** - 
![image.png](/.attachments/image-13a5dd7c-d074-4fb3-8a62-e9d77651ce5e.png).

Java service approach directly to Audit Service API's.
it's records changes in cases, entities and etc in data_audits. it's saves old value and new value.

java services olso responsible on federated search and it sends records of search queries to queries_audit , using Audit service API's. :

![image.png](/.attachments/image-01764877-2ed9-4071-95b8-e43324b94381.png)


