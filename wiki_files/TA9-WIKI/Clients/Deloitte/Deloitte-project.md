# PROJECT OVERVIEW


This project focuses on collecting and analyzing data about companies, shareholders, executives, and their relationships. 

![image.png](/.attachments/image-0939fe26-9a88-4be7-9746-3a6241efb897.png)

1.  **Dashboard** – A tool for managing and analyzing information about clients, companies, and shareholders, including ownership data, financial ratings, and business alerts.
    
2.  **Data Collection Process** – Includes data retrieval from external systems that provide information about companies, controlling parties, and executives. The data is collected from multiple sources:
- **DnB Israel** – Provides information on Israeli companies, including DUNS numbers, ownership structures, credit ratings, and more.
- **Lexis BI** – Supplies data on individuals and companies in financial and business contexts.
- **Hoovers** – Used to identify the global parent company when dealing with foreign ownership.
    
3.  **Entity Categories** – The dashboard classifies companies and individuals based on various criteria, such as company type (private/public/foreign), ownership percentage, executive roles.
    
4.  **Data Paradigm** – All data is collected in a specific structure, and to generate CSV files for automatic loading.
    
5.  **BI and Data Analysis** – The dashboard tool enables analysis and expansion of information across different models, with the option to view additional details.
    
6.  **Data Validation Process** – Each data model includes an “Is Verified” field, allowing users to verify and mark data that has been checked.
    
In summary, this is a dashboard designed to provide a view of ownership structures and financial risks of companies.

## Functional Flow

- Start with Research request model​   
- Moving to any other model is supported using identifiers​
- Analyst can add/update data along the process, finalizing the report like – hide irrelevant owners, or mark “valid” for lexis entities​
- Export is supported in any step of the way​
- Data can be viewed in the dashboard to see the “bigger picture”

![image.png](/.attachments/image-d740ea7e-83d9-4aaf-8e15-d6055836e537.png)

## relevant links:

Deloitte dashboard - v21
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B00F45AD6-5644-49CC-84D1-7EC2A01A40C5%7D&file=Deloitte%20dashboard%20-%20v21.docx&action=default&mobileredirect=true

Deloitte - Demo meeting - 22.12
https://ta9comp.sharepoint.com/:p:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B58C89B6C-41B3-436E-850E-428F2CB68265%7D&file=Deloitte%20-%20Demo%20meeting%20-%2022.12.pptx&action=edit&mobileredirect=true

PRD
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7Bfbca0a2b-07cf-47d8-b8b7-110dab818993%7D&action=edit&wdPid=41509c99
