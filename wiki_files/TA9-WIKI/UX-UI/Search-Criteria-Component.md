**General Information:**
The search component is the main essential component in every data model. 
Today's design:
![image.png](/.attachments/image-7c7e7556-c1bd-452d-b9ce-6d343cbebe48.png)
This chapter will describe the guidelines of the new design, improving both interface & experience.

---

**Link to Mockup & Assets:**
https://xd.adobe.com/view/3c2b298e-58cc-4b19-4a45-a05a699ef3e7-4a1a/
---

**Design Goals:**
1. Improve UX when searching:
   - Allow saving criteria properties
   - Allow sharing criteria
   - Allow recurrence
   - Use Query builder abilities combined with advanced search in a single place

2. Improve the appearance of the main search component for Data models
--- 

[[_TOC_]]

--- 

##**1.0 Search bar design** 
This will be the new search bar design: 
![image.png](/.attachments/image-f14a3c77-2273-44dd-a48c-8debc8f7898b.png)
**Notice that there's no "advance" button

To run a query the user will insert a value in the search bar and will click the magnifying glass icon.
Normal state:
![image.png](/.attachments/image-4e15eff1-6eff-499e-ac8b-e5f13716b265.png)

On hover state:
 ![image.png](/.attachments/image-1615c240-5414-4d06-a2ce-08b0fcf50553.png)

--- 
##**2.0 Using the Advanced filters**
- - When the user opens the "Advance" menu, the options window will cover above the main search bar, hiding it like so:
![image.png](/.attachments/image-f20bb76b-c603-405a-a632-59d5fb53f546.png)
- Notice that a **Secondary search bar unit** is now injected to the "advanced" window, above the conditions 
- Notice that the **Main Search bar unit** in the background is grayed out.
- This design should be implemented to the new Query builder as well:
![image.png](/.attachments/image-9c6d29e1-6443-46e7-8eab-1b5c32ebc4fc.png)
- This design, was meant to give the users the possibility to save the **“Search phrase”** along with the conditions.
IMPORTANT:
If a user types in a search value and/or Chooses identifier, and than opens the "Advanced" - the value should be copied to the secondary search bar and vice versa.


###**_2.1 Quick Filters_** 
The advanced filters (AKA Quick Filters) will now contain a new condition:
- _Case_ - allows to search by case by default when data model is managed

*Defining a quick filter should only be allowed on lookups / distinct fields to avoid the system from crashing.
**When a user clicks the "Drop Down Arrow" on a quick filter, the system automatically should bring the first 100 results with a "**Show More**" for more options in bulks of 100:
![image.png](/.attachments/image-bb1334bd-2c4d-4538-a307-b0cdaf761d6f.png)
If the user start typing than the dropdown will show the relevant choices according to the written text (%).

When clicking the arrow the interface will be displayed:
![image.png](/.attachments/image-bd8d71c4-3adf-4b1d-a04a-34ee868d4591.png) 
- The advanced search definitions will be exposed to the user (Those settings are configured per each data model by the system admin from "admin studio").
- "Run" executes the search, only active when at least 1 condition is filled.
![image.png](/.attachments/image-cadf873d-30f8-4aa5-8ecb-15228eae20a6.png)
- Changing the operator affects the value fields:
![image.png](/.attachments/image-842edac7-b883-4a0a-bb03-a39d0b7b8813.png)
- Choosing a location will be displayed like so:
![image.png](/.attachments/image-058e9339-5c4b-4003-8cc7-d2eb02395d4e.png)


###**_2.2 Saved Criteria drop down_** 

![image.png](/.attachments/image-40ad4461-2990-407a-ba48-b53625577659.png)

- Holds all saved criteria (Saved or shared) 
![image.png](/.attachments/image-105d63ca-9401-47e9-981e-8ede6ff01239.png)
- Clicking the drop-down arrow ![image.png](/.attachments/image-6d451dc6-fab8-43cb-80b4-9efde9c27f60.png) will close the list returning to the "advanced search" screen. (see behaviour in the mockup)
- Th UI Allows search by name 
![image.png](/.attachments/image-f80bcc5a-1923-401c-b782-e548377b7d5b.png)
- The list is filtered while typing:
![image.png](/.attachments/image-ff36fa27-3fbe-4cc5-9c95-77e9c198eacc.png)
- When the mouse cursor hovers over saved criteria it gets marked with a blue background:
![image.png](/.attachments/image-89454970-d844-41ff-a484-d53f7b67e494.png)
- Clicking the trash![image.png](/.attachments/image-9deee4e6-cafd-45b4-a2ce-ccf8df767a20.png) will present a pop-up warning:
![image.png](/.attachments/image-e98ef3ba-87b5-4780-9296-f1e509260647.png)
- Clicking on the search Icon ![image.png](/.attachments/image-4e6cdd7e-b7dc-4d87-9593-4e7a1fa77d79.png) will run the search
- Clicking on any saved criteria will forward to the "Saved Criteria page", showing its search values:
![image.png](/.attachments/image-8a67c3a2-fb8b-433a-b782-d6ce05929604.png)


###**_2.3 Advanced Search condiotions_**
- Add new conditions for the search by using these controllers:
![image.png](/.attachments/image-6d598d73-27ea-488e-b3ab-2449ff611ef5.png)
(Works like the query builder)
- When more than 5 search conditions apply on the GUI, an internal scroll will be activated. (within the white box) the header and footer of the window should not be scrolled
![image.png](/.attachments/image-67ce3247-13a6-4ef0-90c6-271b51eb5efd.png)

For each search controller - there might be several layouts. For Example:
- Date - Last week:
![image.png](/.attachments/image-64d3af29-29a8-47e8-afe8-cfc694b3a7bd.png)
- Date - Between dates:
![image.png](/.attachments/image-0ad9a925-21bb-466b-bca8-fbe988b45ef3.png)


- Location - Has a button ![image.png](/.attachments/image-1e1d185d-c01d-4b8b-af89-e4ccb53c6340.png) to open the map widget:
![image.png](/.attachments/image-7236a9c7-ecea-4137-bee4-5b68773d953f.png)
- After Click:
![image.png](/.attachments/image-864f2351-d0ce-49df-b629-28102f84329d.png)
- After marking a polygon, the "polygon1" title will be written in the textbox:
![image.png](/.attachments/image-a5b2d367-b221-42f6-aa71-b39a04114ab9.png)
- Clicking the trash icon ![image.png](/.attachments/image-e20be355-4072-4b37-a841-b4eac65fde71.png) will clear the form to an empty state
- Clicking the ![image.png](/.attachments/image-15cbe5a8-aa85-4a43-ab12-0712203070fc.png) will temporarily remove the filter. It will re-appear in the UI if the user will reopen the "advanced" window.

###**_2.4 Advanced window Footer_**
The Most basic state of the Advanced search footer is as following:![image.png](/.attachments/image-ad611eda-4392-4edd-acb2-2976c11e0b40.png)

- "**Run** - executes the search
- **Save** - will allow saving these conditions as a criteria
- **Clear All** - will clear all filters and will open a new "Query Builder" state:
![image.png](/.attachments/image-a769a2f1-a097-4b0a-a85a-8c9f1d614577.png)

###**_2.5 Query Builder_**
- Functions exactly like the QB today. No behavior changes.
- The main change is that the UI should be contained within the popup.
- Clicking the "Clear All" will display a clean Query builder UI:
![image.png](/.attachments/image-aefe7c05-b46e-4496-9608-698ebfd70822.png)
- On QB Mode - The title changes to Query Builder + Light bolt icon:
![image.png](/.attachments/image-480ae069-ad91-46e6-b728-62bfe5c21b98.png)
- On QB with results the user can click on "Cleare all" to  start over with a new form:
![image.png](/.attachments/image-d93e9b7e-2226-45bf-9716-5632eae3a6f2.png)

####**_2.5.1 New Query Builder capability-Results Range_**

- _Results Count_ - Allows limiting the returning results (More than, less than) 
![image.png](/.attachments/image-bd543fcd-d7f3-4fb5-ba65-16128c475fdb.png)
The user may fill in the range of results, or only use one condition:
![image.png](/.attachments/image-0f5a1eab-ade7-405a-aba6-c035a6049631.png)
OR
![image.png](/.attachments/image-2a147e15-208d-41c4-b1d6-76e2907688ea.png)

---
##_**3.0 Save a new criteria**_
Saving new criteria can be done in both ways:
a. From the Advanced search filters by clicking "Save As"
b. From the "Saved criteria window by clicking "Save a copy"

Each saved criteria has a different set of values + Metadata.
###**_3.1 Steps of creating new criteria_** 
- First, the user defines the search conditions (from an advanced search or query builder).
For example, calls longer than 12 seconds, in the last week:
![image.png](/.attachments/image-f2ce50f8-0cf8-4b48-b242-8be11053a008.png)
- Now the user clicks ![image.png](/.attachments/image-bdefbfee-6ca8-41ad-8720-98d4196038b8.png)
- The "Save criteria as" screen will pop, asking the user to insert the metadata:
![image.png](/.attachments/image-b4cb941b-c909-454a-bd92-1c20b942b6c8.png)
--  Name (Mandatory field) Max charts = 60
-- Description (Scrollable) Max charts = 500
-- Color
-- Visibility status (Private / Public) - Private by default
- The user will complete the action by clicking the ![image.png](/.attachments/image-ed65f38b-8027-4fb8-b560-932fa3cf33fb.png)
The new Saved criteria will be saved and can be accessed from the main list: 
![image.png](/.attachments/image-65af2384-c5c2-4750-b698-780acac73b15.png)

![image.png](/.attachments/image-1212bef7-3a88-4851-921e-d4e1415cc61b.png)
- The list also informs the user of the last execution date, and if a criteria is recurrent or not.

###_**3.2 Saved criteria screen options**_

_a. Header section_ 
- Set Automatic recurrency ![image.png](/.attachments/image-581a3104-7ffc-4b77-b93b-539439ecc6dd.png)
- Edit Criteria meta data ![image.png](/.attachments/image-8d7c8e32-727e-4dcf-b03d-9a38d34bfc1a.png)
- Save ![image.png](/.attachments/image-b7c23ae4-310c-4f98-bbe9-e912f32fd26f.png) - Clickable only if changes where made
- Criteria name appears on the top left, with its color.

_b._ Criteria conditions
![image.png](/.attachments/image-3ef278f0-6941-46fc-a910-72600879b1b1.png)

_C. Footer - Action buttons_
![image.png](/.attachments/image-e9c70765-c370-48b8-8c03-f7aee8705002.png)
- Close - Returning the user to the Main screen with "advanced" quick filters
- "Run" - Executes the query (Ignores unfilled/empty conditions)
- "Save as new" - Create new criteria based on the current conditions & metadata:
![image.png](/.attachments/image-f360cc58-884d-47f6-bb98-72846d9d47d5.png)
*** NOTICE - The word "**New**" had been added to the "Criteria Name"

###_**3.3 Sharing Criteria - Public**_
To share criteria with others, it needs to be set as "public" from the edit mode![image.png](/.attachments/image-c9cd74aa-2a9d-40ac-a1e3-ba3cea8a28b0.png):
![image.png](/.attachments/image-27f0cce2-9730-4afd-959a-17fac1a34c9a.png)
Once the criteria are set to  "public", 3 drop-down (Multivalue) lists will be seen in the window allowing us to choose with whom to share:
- Group - allow sharing with a group of users
- Users - Allow sharing with individual users
- Rolls - Allow sharing with a group of users with the same roll
![image.png](/.attachments/image-a659bb15-eed1-4a6d-9f61-ca46a4f8d57e.png)

When a certain list is Clicked on, a multi-choice menu is opened, asking the user to choose with whom to share. 
Once done, the user will click on "ok" (top right) to approve the selection.
![image.png](/.attachments/image-bb254a7d-761c-4f3a-ac03-4ecd2d35190c.png)
Finally, the user needs to click on "save" to approve the sharing definition:
![image.png](/.attachments/image-e61fee8e-1971-411b-8dcc-ca923bec34a2.png)
The shared users will gain access to the criteria from the "Saved criteria" list.

###_**3.4 Delete criteria**_
To delete criteria - the user needs to click the trash icon![image.png](/.attachments/image-8f434da6-f8bd-4369-9e34-0d3a047aef6c.png) from the "saved criteria"  dropdown: ![image.png](/.attachments/image-dfd7d148-e8ee-4cdf-bdd5-7aaa2e67ee70.png)
or from inside the criteria screen:
![image.png](/.attachments/image-b4edd31e-ea02-4601-adcb-2a0f55615981.png)
After the click, a warning message will appear asking the user to approve deletion:
![image.png](/.attachments/image-687f813b-83a6-4cd0-b7d4-1548f1e316cf.png)
- "No" - will close the warning message, returning the user to the previous screen
- "Yes" - will delete the criteria from the database (removing it from the list). 
- Only the "criteria Owner" has the ability to delete criteria

###_**3.5 Recurrency**_
- To set a recurrency, the user first needs to choose the criteria.
- Once a criteria is chosen, the user will click on the "recurrence" icon: 
![image.png](/.attachments/image-7666e048-332d-4316-8424-266b6973eb29.png)
- Recurrency will only be available for 1 user on phase 1. The receiving user name will be added as the "Assignee".
- Users may change the assignee and direct the results for a different user.
- Default assignee will be the creating user
- The Assignee has to be a user from the "shared" list
- The recurrent settings window is now seen, for that criteria:
![image.png](/.attachments/image-9227b506-fd62-41a0-94c3-f8c91909e8d9.png)
Steps to make recurrency:
1. Choose the time range (Start > End) - the end date cannot be before the start.
2. Choose the time of day- the user can choose one or more time slots. - mandatory at least 1.
![image.png](/.attachments/image-d5f76b19-3e80-471c-9109-8480784aa0c4.png)
2a. Choose Weekdays - "All" will be selected by default. The user can pick specific days:
![image.png](/.attachments/image-d91c306d-2967-47a7-bee0-2adaf4acd7cd.png)
2b. Choose Monthly days - "All will be selected by default. The user can pick specific days:
![image.png](/.attachments/image-e63b314a-303f-4890-9e63-fc722f830b19.png)
![image.png](/.attachments/image-075ac415-35e0-4d4b-8377-fcb2a601734a.png)
![image.png](/.attachments/image-8662e1bd-eb8f-4dee-b97a-a3207e5d6ee3.png)
3. The user will click on "Save" to save recurrency:
![image.png](/.attachments/image-0e7778c6-ede7-40bc-8b97-464aeb85582b.png)

Finally - recurrency setting is saved, the screen goes back to the "criteria" screen showing the recurrency icon in blue - for "On":
![image.png](/.attachments/image-20336145-03cc-45df-a232-f27b05ce9879.png)

To remove the recurrence, the user will click the blue icon ![image.png](/.attachments/image-d91f5357-7c7b-4594-9bc5-fb4c7d67b3ca.png) going back to the settings screen, and will click on "Remove recurrence" from the footer:
![image.png](/.attachments/image-49eeca8c-2406-49ba-ac61-d408e044e652.png)

A warning message will appear asking the user to approve the removal of the recurrence setting:
![image.png](/.attachments/image-9c7d16a4-7e80-4dbb-a5db-1fed83bce2f5.png)
- "NO" - will close the warning message, returning the user to the previous screen
- "YES" - will remove the recurrence from criteria. going back to the previous screen

4. Scheduled Criteria permissions
- The creator of the scheduled criteria is the only one allowed to edit / change / remove the recurrence
- Any user that was shared with criteria can set recurrence for it for himself or another user

####_**3.5.1 Saving Changes / Edit criteria**_
- When a user is changing existing criteria, it is required to save the changes before he closes the criteria settings page.
Therefore - the system will alert on changes that weren't saved before leaving the page:
![image.png](/.attachments/image-59e177e4-3cdc-4e6b-83d0-766c3cc51070.png)
"X" - Closes the notification, without taking action. Returning the user to the Criteria page
"YES" - Saves the changes, completing the action
"NO" - doesn't save the changes and complete the action

####_**3.5.2 Execution**_
Once the criteria executed, the data model will return results. The Search UI should remain on the same executed criteria.
To cancel the criteria condition the user should click on "Close"


###_**3.6 Permissions**_
- The Creator of the criteria can, Edit, delete and share
- The person Shared with can View only
To add The "creator" permission to a user - The system admin will be able to give such permission from the admin studio. 

##**4 reports & output destination**
The system will contain A new folder (named as "**Search Criteria**") in the Data models module to hold 2 new system data models:
- My Criteria - Will contain all of the user's owned/shared criteria
- My Reports - Will contain the user's created reports
https://xd.adobe.com/view/82270e4d-20f9-403f-945f-d6d19a6bf397-d774/

Folder access:
![image.png](/.attachments/image-3e40ec2e-deb2-4a32-b878-7097203e5952.png)
![image.png](/.attachments/image-1fb8d96a-787d-4029-aadb-d78012db3a3d.png)


###_**4.1 My Criteria**_
A designated data model storing the user's owned/shared criteria:
![image.png](/.attachments/image-7e316e0e-bcfa-47f1-bdf8-7ae17057a496.png)

Schema fields:
- SysID - An ID given to the criteria (Identifier)
- *Edit - Open the criteria settings in a modal - to allow editing.
- Color (display the color given to the criteria)
- Criteria Name - Given by the creating user
- Criteria Description - Given by the creating user
- Linked Data model
- Creation date 
- Owner - Creator
- Last update date
- Updated by - The user who did the update
- Last run - (Date/Time of last run)
- Visibility - display if it's Public/Private
- Shared with - If "Public" displays the usernames (multivalue)
- Is recurrent - Y/N Boolean
- Recurrence start date
- Recurrence end date
- Recurrence time of day (multi Value displaying the hours)
- Recurrence on (display either Weekdays / Monthly days)
- Recurrence pattern (multi Value displaying the configuration of week/monthly days)


*when clicking the "edit" icon (![image.png](/.attachments/image-69bb2b38-2c44-4eba-9153-edbde0b2beca.png)), the criteria settings should open in a modal window:
![image.png](/.attachments/image-50631f48-d513-400d-9ef1-11f4022ef22d.png)- allowing the user to edit and save the QB settings
- Add/remove recurrency
- edit name, description, color & visibility
- delete 
- Save as a new criteria


###_**4.2 My reports**_ 
A designated data model storing the user's owned/shared criteria results:
![image.png](/.attachments/image-20e97f13-e0a3-4819-bb92-39a35a632138.png)

Schema fields:
- SysID - An ID given to the criteria (Identifier)
- Status - New / Viewed
- Color (display the color given to the criteria)
- Criteria name
- Criteria description
- Linked Data model
- Last run - (Date/Time of current run)
- Number of results 
- Open (button to open the results page)
- Next run - if recurrent - show the time of next run
- User - Creator
- Assigned user 

####_**4.2.1 My reports - Behaviour & Actions**_
- Sorted Descending by default - latest criteria results should be on top
- New results will be marked by using **BOLD** FONT + "**New**" in the status column
- Once results where viewed, the "New" will be replaced with the "Read" icons (![image.png](/.attachments/image-060b07ec-db3f-434f-8b2f-caeffd99a3ef.png))) - Define per user
- When Clicking "Open" icon (![image.png](/.attachments/image-7f3357bd-757a-4861-a2f8-da8f5f8405c8.png)), the results will be opened in a new tab
- Right-clicking on the checkbox will open the "options" menu allowing the user to
![image.png](/.attachments/image-5718a1d3-78b8-4622-bfa4-977121010f19.png)

** Send to Federated

** Share - Will open the Sharing Modal
![image.png](/.attachments/image-63010285-11f9-4f28-be86-b0aabd7cd83c.png)


**Delete row/rows (The system should display a modal asking the user to verify delete)
![image.png](/.attachments/image-2baff760-97a7-4696-b9c7-87492a31fc64.png)

####_**4.2.2 My reports - Share to case**_
- By Sharing results to a case - A Results file will be sent to the case, will be displayed in the "Data" tab like we have today:
![image.png](/.attachments/image-62965e7f-7cf3-4b4f-9b69-728c45ebb550.png)
- Sharing settings applied on the criteria should remain and be presented.
- If multiple rows where selected, the action will apply to all selection.
- A user will only be able to share to cases he/she has permission to

####_**4.2.3 My reports - Recurrence Alerts**_
*Assigned user will be getting a notification to the Feed widget in the personal portal
- In the future users will be able to get the notification by mail
