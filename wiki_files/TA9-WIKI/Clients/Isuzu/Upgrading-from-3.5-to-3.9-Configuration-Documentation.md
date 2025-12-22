After a successful upgrade to 3.9 The Following configurations needs to be done:

**1. Update link analysis default template:**
Wiki: https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/627/Link-Analysis-Templates-Script
Ticket: 
Description:

---

**2. Update departments config:**
2.1 Dll config 
Ticket: 
Wiki: 
Description: configuration in the users management dll to support the new departments organizational unit

2.2 Active directory config 
Ticket: 
Wiki: 
Description: Configure the departments organizational units

---

**3. Update Case profile for all users:**
Wiki:
Ticket: 
Description:

---

**4. Remove Face recognition app permission to all users:**
Wiki:
Ticket: 
Description: To avoid the permission to cause force log out from The application

---

**5. VMS Video Configuration:**
Wiki VMS Mock config: https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/643/Vms-Get-VMS-cameras-Mock
Wiki VMS TA9 Config: https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/637/VMS-IntSight-Connection
Ticket: 
Description: Configuring the VMS feature

---

**6. Large Cellebrite files configuration:**
Wiki:
Ticket: 
Description: Configuring the folder for dropping large cellebrite zip files

---

**7. Entity Extraction engine configuration:**
Wiki:
Ticket: 
Description: Configuring the system to work with the new EE engine from Azure 

---

**8. Speech to text and Translations configuration:** 
Wiki:
Ticket: https://dev.azure.com/ta-9/Argus/_workitems/edit/44171
Description: Viewers, service password,custom paths, ports/url to open etc (NEED TO ADD DESCRIPTION)

---

**9. My Reports Data model configuration:** 
Wiki:
Ticket: https://dev.azure.com/ta-9/Argus/_workitems/edit/44171
Description: Make sure the data model is configured properly

---

**10. Scheduled criteria:** 
Wiki:
Ticket: 
Description: Make sure the saved criteria report opens 

---

**11. Base Translations:** 
Wiki:
Ticket: 
Description: Copy the translations from 50

---

**12. Type & Sub type for cases:** 
Wiki:
Ticket: 
Description: update the list of types and subtypes like the client sent us with dependencies. if needed ask for newly updated list.

---

**13. Dynamic location definition on CDR data model:** 
Wiki:
Ticket: 
Description: Define dynamic location setting on CDR groups (from / To)

---

**14. Case Export - DocX and PDF:** 
Wiki:
Ticket: 
Description: Make sure the case summary tab is exported on both formats in the designed template

---

**15. Reports configurations:** 
Wiki:
Ticket: 
Description: Make sure that all reports are configured properly, with quick filters, and match 50 / stage to look like prod.

---
**16. Snapshots of configurations. TBD**

---
**17. Face recognition permission:**
Wiki:
Ticket: 
Description: In order to remove the permission to face recognition app for all users run this sql query: `update  sqlite_metadata.usersensors set isActive=0 where sensorID=7;`

2.remove the identifiers 'Face' and 'Detection' from person entity . 
---
**18.VMS request DM - autorun:**
Wiki:
Ticket:
Description: In order to make the 'vms request' DM to run automatically - Go to the admin studio ->  Data models -> VMS Request DM -> Repository -> click on 'auto run on startup'.

**19. VMS other configurations**
Ticket: https://dev.azure.com/ta-9/Argus/_workitems/edit/44195/

---
**20.Situational Awareness config:**
Wiki: https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/635/Situational-Awareness
Ticket: 
Description:   

---
**21.Tasks App:**
Wiki: 
Ticket: 
Description: Create task app from the admin studio.
App URL - http://intc2-stg/#/report/-30
Mode - Link
Open As - Replace Current
Add image 
Configure Status Changes on Drag And drop (IT)
Configure double click on kanban opens in popup (IT)
---
**21.Images and Icons:**
Wiki: 
Ticket: 
Description:
- add image - Situational Awareness app
- add image - Tasks data model
- add image - hora data model
- add image - transcript app
- add camera icon - camera DM
**images folder** https://ta9comp.sharepoint.com/sites/businessteam/Shared%20Documents/Forms/AllItems.aspx?csf=1&web=1&e=lDUZAD&cid=f9a513d0%2Dae17%2D4b9b%2Da4c1%2Ddc3b0357a37f&FolderCTID=0x0120007A9A1DC3444F3A4BBE9B7CD696FBDC5C&id=%2Fsites%2Fbusinessteam%2FShared%20Documents%2FProduct%2FDM%20pix&viewid=671b21c4%2Da9c0%2D4c50%2D968c%2D1d4447259543

---
**Departmets**
Wiki:https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/576/Create-Department-and-Users-Active-Directory
Ticket: 
Description: Add the configuration of the departments to the user management service dll
---
**22.uploading translation update files:**

Wiki: 
Ticket: 
Description:
1. make a backup table of the current translation table which is called sqlite_metadata.language_translation, to do that run the next commands:
CREATE TABLE new_table1 LIKE sqlite_metadata.language_translation; 
INSERT new_table1 SELECT * FROM sqlite_metadata.language_translation;
CREATE TABLE new_table2 LIKE sqlite_metadata.language_translation;
2. import the new translation file to a new table as well just so you have backup by running the next commands:
LOAD DATA local INFILE 'C:/..../...csv' (file location locally)
INTO TABLE new_table2
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
3. join the new table to the old table by key by running the next commands:
update new_table2 
left join new_table1 
on new_table2.ItemKey = new_table1.ItemKey
set new_table2.Trans_2 = new_table1.Trans_2
WHERE new_table1.Trans_2 IS not NULL
4. you're done! just make sure the new translations were added to new_table2. when you're done with that just change the name of new_table2 to language_translation and that's it!