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

