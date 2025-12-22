To Delete a case from the database:

1. Locate CaseID (Investigation ID). It is written in the case URL in the web application:
For example: ![image.png](/.attachments/image-09b1b287-420e-48c6-8fc7-c4467a17e3ba.png)
**Case ID = 555**


---

2. Go to the SQL and type the following command
Delete from sqlite_metadata.investigationheader where InvestigationID= "X"
*replace the "X" with Case ID.

---
3. Run the command, validate deletion in the SQL scheme and web application.
