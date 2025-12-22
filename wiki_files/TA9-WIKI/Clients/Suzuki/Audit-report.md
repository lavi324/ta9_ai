#  Client requirement  
  

**1. Audit Report – Available Today**  
Our platform already includes a data model called **“query audit”**, which captures all query-related audit data in TA9.  
You can use the **“group by”** functionality to view and group records by user (by dragging the login name column to the top).
*   The first screenshot shows the grouped records per user.
*   The second shows the detailed view when a specific user is selected.

![==image_0==.png](/.attachments/==image_0==-df11c3c0-800f-4966-9641-91332ebdf682.png) 
![==image_1==.png](/.attachments/==image_1==-87968d9e-0348-4ca6-90e9-3a38be22e8ba.png) 

**2. Customized Report Plugin – Optional Development**  
This part of the requirement involves generating a custom report with a specific UI layout and combining data from two sources: the TA9 audit data and Active Directory (e.g. supervisor details).  
To meet the request, you can develop a custom external plugin, similar to the person report you have. This plugin would fetch data from both the **query audit data model** and **Active Directory** using logcomplexquery and present it in the desired structure.
This approach allows you to tailor the report to your specific needs.

# Concept:
PR - existing person report
AR - requested audit report

![image.png](/.attachments/image-f9ebf344-5f55-461a-97b0-f77ecced0748.png)

[Audit_report_change_v1.0.3.pptx](/.attachments/Audit_report_change_v1.0.3-eba6ed2c-d5c2-40cb-9ff1-495395b0f081.pptx)