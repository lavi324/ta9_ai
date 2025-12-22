This feature was designed to support deloitte's workflow to allow full data fetching per company\person, allowing joining data from multiple DB's, based on preset terms, using a company\person ID or name.
This feature is an initial version to a wider solution for harvesting data workflow.

::: mermaid
 graph LR;
 A[Data model change trigger to start an action] --> B[Inserting data in a another data model] --> C[Data harvesting in another data model/Inserting data in a another data model];
:::


3 new services were designed in order to support the following process:


![image.png](/.attachments/image-6a0c2c05-786e-4ae2-a410-361b69bab97d.png)
## **Workflow ActionsSPI service:**
Each Action will be stand alone

2) Actions will not be dependent

3) All actions should inherit from "base action" that will impement basics interface and common methods.

4) Dispacher per Action.

5) Action wil response a new task to tasks queue

6) ActionsSPI will listen to actions Queue

7) Action response will include : status, message, actionID

8) Each API in ActionsSPI should have a ticket, a fully testing postman and unitTest that

9) Each API will be written with it's entire description in a sub task ticket here (except for the 1st 2 demos)

*   This service SHOULDN'T update table!!! (it can get\fetch data for data manipulations - duplications, etc).

## **WorkFlowMgr service:**
1) Pull Requests(workflows)\tasks - MassTransit consumer.

2) Break requests (Workflows) to tasks per DM

3) Break tasks to Actions by DM and it changes

4) Insert\update requests table , tasks table and action table.

5) Insert Actions to action queue

6) Pull statuses from status queue.

7) Update  Actions, tasks and requests statuses - status manager service should be implemented here.


**Notes:**
* In data model request there's no update only insert.

**Deloitte Dashboard solution**: https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B4DE00D32-8E7D-4560-A957-725EF7FC4C8F%7D&file=Deloitte%20dashboard%20-%20v2.docx&action=default&mobileredirect=true

# Troubleshooting

Every row has a row status, if the number doesn't get back any details, the user can search the row status for a message.
The table "WFtask", workflow table of activities in mariaDB metadata the admin can fins all of the actions regarding the workflow, including the row status and comment of the row. 

** No bug fixes at the moment
**Use Case:** Inserting a wrong company name 
