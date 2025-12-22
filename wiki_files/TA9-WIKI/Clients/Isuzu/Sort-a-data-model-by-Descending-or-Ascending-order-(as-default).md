This Tutorial will guide you on how to sort by default a data model in a descending or ascending order.
Basic guidelines before defining:
1. The data model must contain a "Date" column with actual dates
2. The "Date" field needs to have "indexing" on the database

**Steps:**
In order to apply the sorting definition do the following:
1. Go to the "Admin Studio"
2. Choose "Data models" 
3. Choose the relevant data model
4. Locate the "Date" field you wish to apply the sorting
5. On the side properties menu, locate the property "Sort Mode"
![image.png](/.attachments/image-1e01b0cf-46a2-4040-a806-17aee4c43494.png)
6. Set its value to the required sort mode
![image.png](/.attachments/image-55aa4045-45bb-4a63-b82e-ccb9e2b8821b.png)
Desc - Descending
Asc - Ascending
7. Click "Save"
8. Clear server cache

**On the Web client application:**
1. Clear client cache
2. open the data model you just changed (or refresh)
3. Click the Search to run the query


**Validate -**
1. The Data model opens up with a "Sort mode" defined - ![image.png](/.attachments/image-f2175b1f-8aac-4082-b597-a3d2781328a5.png)
2. The Sort mode shows the "Date" column as a value
![image.png](/.attachments/image-75cf392c-d578-413d-9bd2-1101709149a4.png) 
3. The data model is now displaying results in the chosen order.

**NOTE!** - If the data model won't display the results sorted, or if any of the validation steps are missing, turn to your system support for further inspection.