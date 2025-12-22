# Error handling and troubleshooting
The workflow feature now will have the ability to continue the flow after user made changes in the predefined fields: 

1.  Data Model: Owners  
    

- When user Insert a new row to the data model, it will trigger the workflow based on request ID and Owner Type for all types of requests.  

2.  Data Model: Person / Companies  
    

*   When the user Insert a new row to the data model, it will trigger all Lexis actions on the inserted row. This action will insert new rows in the Lexis data models. 
    

*   When the user updates the entity Hebrew/English name, it will trigger the Lexis actions and will insert new lexis data in the Lexis data models. 
    

*   When the user updates DUNS in the data model it will trigger Hoovers (DnB+) API’s and will add data on the foreign company in the Owners DM (Based on Regis) and all other dm’s in the workflow in accordance to the pre-defined logic. 
    

3.  Data Model: Key Executives 
    

*   When the user inserts a new row to Key Executives data model, it will trigger the Lexis actions and insert the received data from Lexis to the Lexis data models. 
    

*   When the user updates the Name field, it will trigger the Lexis actions and insert the received data from Lexis to the Lexis data models.


ticket - https://dev.azure.com/ta-9/Argus/_workitems/edit/52914



## Troubleshooting scenarios
       
| DataModel | fields changed | action to trigger | Description |
| --- | --- | --- | --- |
| Companies | name or name2 | Lexis with editedName | Will triger new Lexis data |
| Companies | All but name\name2 or Regis\Duns\LegalEntityState | none | will update thr specific row data and will not trigger any action |
| Companies | LegalEntityState | GetCompanyAction |   |
| Companies | Duns | DNB+ and lexis | Shouldn't change anything, as the APIs depend on Regis\Duns and therefor the changes will be overwitten |
| Ownerships | Insert new row | In condition to target company need to execute continuesly actions according to table | update will not do anything - as it wasn't configures. How do we know who to update? Owner? Owned? Person? |
| 1) Insert new company with RequestId (for the context) -> triggers getCompanyAction |
| 2) Insert new Person with RequestId (for the context) -> triggers lexis +owned |
| 3) Insert new Ownership row -> Searches Company from companies and sync it into new owners record |
| Person | person name | Lexis with the new name | Will execute the Person flow with the new ID and new info will be attached to the same record as the record id will not change (just the person ID) |
| Key Executives | Insert new row with requestId | Lexis | will trigger only lexis Action . Note: you must enter requestId  as it must run under a requestId context |
| Key Executives | update EmployeeName | Lexis | will trigger only lexis Action . Note: Becarfull with requestId value as it is the Key Executive context. |




## list of companies we tested on for each company type:

        
| Test | Column1 | regis | DUNS | Client Name English | Client Name Hebrew |
| :-- | :-- | --- | --- | --- | --- |
| Consulting  | ישראלית ציבורית | 515546224 | 532107392 | MULTI RETAIL GROUP LTD | מולטי ריטייל גרופ בע"מ |
| Consulting  | ישראלית פרטית  | 513763219 | 514708507 | S. SHLOMO VEHICLE LTD | ש. שלמה רכב בע"מ |
| Consulting  | זרה ציבורית | NA | 204137475 | Loblaw Companies Limited |   |
| Consulting  | זרה פרטית  | NA | 370644123 | Smart Car Repair Group |   |
| Consulting  | יחיד | 17483074 | 533059171 | Shalom Shai | שי שלום |
| Consulting  | עמותה | 520028275 | 600089395 | Israel Museum | מוזיאון ישראל |
| BR | ישראלית ציבורית | 515546224 | 532107392 | MULTI RETAIL GROUP LTD | מולטי ריטייל גרופ בע"מ |
| BR | ישראלית פרטית  | 513763219 | 514708507 |  S. SHLOMO VEHICLE LTD | ש. שלמה רכב בע"מ |
| BR | זרה ציבורית | NA | 204137475 | Loblaw Companies Limited |   |
| BR | זרה פרטית  | NA | 370644123 | Smart Car Repair Group |   |
| BR | יחיד | 17483074 | 533059171 | Shalom Shai | שי שלום |
| BR | עמותה | 520028275 | 600089395 | Israel Museum | מוזיאון ישראל |
| Internal Audit | ישראלית ציבורית | 515546224 | 532107392 | MULTI RETAIL GROUP LTD | מולטי ריטייל גרופ בע"מ |
| Internal Audit | ישראלית פרטית  | 513763219 | 514708507 |  S. SHLOMO VEHICLE LTD | ש. שלמה רכב בע"מ |
| Internal Audit | זרה ציבורית | NA | 204137475 | Loblaw Companies Limited |   |
| Internal Audit | זרה פרטית  | NA | 370644123 | Smart Car Repair Group |   |
| Internal Audit | יחיד | 17483074 | 533059171 | Shalom Shai | שי שלום |
| Internal Audit | עמותה | 520028275 | 600089395 | Israel Museum | מוזיאון ישראל |
| Audit + SOC | ישראלית פרטית  | 513763219 | 514708507 | S. SHLOMO VEHICLE LTD | ש. שלמה רכב בע"מ |
| Audit + SOC | זרה ציבורית | NA | 204137475 | Loblaw Companies Limited |   |
| Audit + SOC | זרה פרטית  | NA | 370644123 | Smart Car Repair Group |   |
| Audit + SOC | עמותה | 520028275 | 600089395 | Israel Museum | מוזיאון ישראל |
| SEC | ישראלית ציבורית | 515546224 | 532107392 | MULTI RETAIL GROUP LTD | מולטי ריטייל גרופ בע"מ |
| SEC | ישראלית פרטית  | 513763219 | 514708507 | S. SHLOMO VEHICLE LTD | ש. שלמה רכב בע"מ |
| SEC | זרה ציבורית | NA | 204137475 | Loblaw Companies Limited |   |
| SEC | זרה פרטית  | NA | 370644123 | Smart Car Repair Group |   |