
[[_TOC_]]

## Update Telco Dashboard Widgets

## Original Template file:
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/Shared%20Documents/Projects/Mapping%20%26%20config/Export%20Templates/dashboard%20template%20telco.docx?d=wf6dcaabe09024d7cba485332cb6fd1f6&csf=1&web=1&e=1ANGfg


### Goal
 Edit Telco widget's names, order, translation, DM ID, visibility, and more
>**Note** - The Link analysis widget should not appear in the template based on a requirement from the client 
https://dev.azure.com/ta-9/Argus/_workitems/edit/40450


### Steps
Open the '**dsb_dashboard_definitions**' table in MySql in the relevant environment
search for the Telco Dashboard row and open the text written in the Layout field 
![image.png](/.attachments/image-94c47027-62fb-4b90-9410-8798f432cc9e.png)
Then, edit the Jason text of the Dashboard description as you want
![image.png](/.attachments/image-17a84aa8-15c9-4942-aab2-fc0c17a10a55.png)
To help you see the text better, you can use the [beautify JSON web app](https://codebeautify.org/jsonviewer) which looks like that - 
![image.png](/.attachments/image-d33751e2-cfb2-4cec-b73c-f509a8b999be.png)

### Options
- delete the entire widget from the dashboard visibility
- change the title of the widget
- change the order of the widgets
- redirect the widget to the correct DM ID by changing the schema's number
- change the skin of the widget by changing the skin's number 

# Upload the file to desired server
Link to webinar: https://web.microsoftstream.com/video/20b8fdea-b297-44ad-862f-797561409180
Webinar aid file: [Windward-Webinar.docx](/.attachments/Windward-Webinar-6d307e7d-1cfa-42b0-b489-e83e8534a746.docx)

![image.png](/.attachments/image-ec4ec5f8-3a00-4e2b-a47b-ae9a787ab0e1.png)

Isuzu/Hof-Template-Final-X.X.X.docx

Download to your PC.

## Upload via web 
![image.png](/.attachments/image-f164e06f-010e-477b-bbea-282cf6b0777d.png)

**Upload The File**

![image.png](/.attachments/image-20f005c3-49ec-44d0-a0c2-90f8a69f1624.png)

## Update SQL Server 

**look for**
*.*load_files

**SELECT * FROM sqlite_metadata.load_files order by id desc;**

Copy the: Serverfilepath 

![image.png](/.attachments/image-1803220a-07dc-4b05-ad1e-aff8622b2dd9.png)

**SELECT * FROM sqlite_metadata.system_config;**

to: Config Value in:

![image.png](/.attachments/image-f1287d74-e47d-446a-bcc4-7c66ef8f1c1c.png)

## Redeploy Wildfly

Delete the deployed file, wait until status changed to undeploy, 
delete again - see status deployed.

![image.png](/.attachments/image-f101c236-63ea-46d3-9c28-92de85ee196f.png)

# Export report is not showing results - troubleshoot


What to do in case the exported report isn't working as expected.

**Test 1 - Validate download**
Make sure that the download starts.
If not - restart the services from 90 in the following order:
- restart ReportsGenerationService (machine 91)

- Restart TA9 Service Host (Machine 90)

Validate: The report is downloading 
If not - escalate to tech support by TA9 OR review the following chapters:
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/208/Troubleshot
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/108/Isuzu?anchor=report-isn%27t-being-exported-in-the-system
---

**Test 2 - If one widget or more do not show results**

If a widget doesn't present results - Make sure the title of the widget is written correctly, and it's **identical** to the data model's name. First, we need to validate if there is data to present by running the data models with a query or trying different search criteria or date range. 
If the data exists, do the following steps:

- Open admin studio, and locate the widget's data model
- Copy the data model name
- Open the IntSight Web application, open telco dashboard and run it
- After dashboard display results click on the pencil icon from the top toolbar to enter "edit mode" ![image.png](/.attachments/image-cd65dd83-9eac-431f-9317-11d331f0c88f.png)

- Go to the "broken" widget and click on "settings icon" ![image.png](/.attachments/image-b9ecb7f6-e67f-48d1-9af1-98d6b8cca01d.png)
- Paste the data model title in the "title" spot
- Click Ok
- Click the green "Save" button to save the changes
- go back to "view" mode by clicking the eye icon from the main toolbar
- Run the dashboard again

Validate: The "broken" widget should display the results
If Not - Escalate to project manager or support partner by TA9.

---

**Test 3 - If the exported file does not display results for one widget or more**
If the exported report shows no results for one or more widgets, we need to make sure that the title of the widget, is **identical** to the title written it the "export template" file.

Step 1: Download the template report from X
Step 2: Update the title as needed - make sure both titles are identical (both template and widget, according to the widget)
Step 3: Upload the report new template file, replacing the older
Step 4: Validate
- Clear cache and hard reload
- Run dashboard again 
- Click export and review the results
- If the title has the ' character in the title, it shouldn't be put in the template. It should be put **only** in the widget itself, in the client.

For more information: [Isuzu Dashboard trouble shot](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki?wikiVersion=GBwikiMaster&_a=edit&pagePath=/TA9%20WIKI/IT/Isuzu%20Dashboard%20trouble%20shot&pageId=516)