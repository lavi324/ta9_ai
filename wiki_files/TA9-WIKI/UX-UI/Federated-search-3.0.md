**Assets & Mockup**
Mockup: 
https://xd.adobe.com/view/b5436904-572a-4ef0-b604-c54363ed1c97-e010/

Specs: 
https://xd.adobe.com/spec/3d104180-753d-4db2-60c8-f3108ef3f094-4b21/

Previewer specs:
https://xd.adobe.com/view/3b304378-157b-4950-61a1-3795317b9e72-4d01/

Sort Results:
https://xd.adobe.com/view/e00fced9-2c41-479e-8b77-e458ab798380-b55c/

Loading Bar Design:
https://xd.adobe.com/view/0b55593a-4a54-4ac8-bb3e-880dbd2556d2-5e06/

Advance Filter Design:
https://xd.adobe.com/view/d82d4290-3e56-430c-859e-5ae21f83e0e2-8d7e/

**Development Plan**
Develop each component according to this order.
Once approved, move on to the next component in the list.

**Phase 1**	
-	Main Screen (Home)
-	SERP

**Phase 2** 
-	Header 
-	New Features
o	Voice Upload
o	Map Tab (Phase 2)
o	Favorites Tab (phase 2)

---
[[_TOC_]]

---

##**1.0 Header** – Phase 2
 
###**1.1 Home Button**
  - Home Button
![image.png](/.attachments/image-06d78ccd-52b5-4876-ac37-1927c1bc4143.png)
   - Home Button Clicked
![image.png](/.attachments/image-5c0b7253-5677-4683-9dcd-bb2b8b9c3c4b.png)
Clicking opens a Navigation Bar, with navigation options to other system screens:
-	Home 
-	Federated Search
-	Link Analysis
-	Map
-	Favorites
-	
##**2.0 Main Screen (Home)**
The Main Screen – AKA Home, is the first opening screen of the federated search module.
It holds the search unit, History unit & search Tips:
![image.png](/.attachments/image-7ae33c3f-396b-4e7c-b3f4-48965cc09570.png)
 
###**2.1 Search Bar Unit**
![image.png](/.attachments/image-2b0bc532-107e-4f7d-a0a4-d2381f352491.png)
 
The search bar is where we will perform searches, by using textual inputs and syntax (Google like).
It supports Auto Complete. 
###**2.2 Image Uploader**
Search Unit also allows: 
 ![image.png](/.attachments/image-7f6ef1d1-1cc8-4bf1-83db-14ba5feb2c05.png) Upload an image
Clicking the upload image opens a Drag n Drop window Below the search bar:
![image.png](/.attachments/image-f6a7867d-525d-4f3c-86a8-6b1452bfe8d8.png)
  
###**2.3 Voice Uploader** - Phase 2
![image.png](/.attachments/image-ee664846-df6f-4cf9-8622-491de4a3097a.png)  Upload a Voice (Phase 2)
###**2.4 Advanced Search**
 ![image.png](/.attachments/image-4ef5892a-b496-4e58-97af-c06f0d7a2550.png) Advanced Search
 ![image.png](/.attachments/image-ac48b86d-25c6-4f0c-8870-42c04713db8b.png)
Each Advanced option should allow a focused search:
Creation Time – Date Picker
Last Updated – Date Picker
Data Source – Multi Choice list
Country - Multi Choice list
Tags - Multi Choice List 
Language - Multi Choice list
 ![image.png](/.attachments/image-23ee7baf-b14e-405c-90e9-f561eecaa6da.png)
Location – Map with a search
Case - Multi Choice list
Clear All – Clean all advanced filters

####2.4.1 Advance Behavior 

1. When No Filters are selected + Advanced menu = Closed:
![image.png](/.attachments/image-4a1221ec-220b-4da4-92e8-4afbcce8ae92.png)

 2. When No Filters are selected + Advanced menu = Open:
![image.png](/.attachments/image-22ce0ad8-dec8-40f9-a1d8-85981f56057b.png)

3. When a filter is selected + Advanced menu = Open
![image.png](/.attachments/image-fa658008-04d6-4686-a251-78fcde533782.png)

4. When a Filter is selected + Advanced = Closed:
![image.png](/.attachments/image-38194683-8ce0-4b16-965f-840513216d7f.png)


###**2.5 Search History**
Support up to 10 previous searches:
 ![image.png](/.attachments/image-c90e8924-0e55-4968-a18c-5dc836191e6c.png)
The User will be able to clean entire history list, or a single search from it:
 ![image.png](/.attachments/image-a4319220-de87-490b-9af5-60f39677b1f0.png)
![image.png](/.attachments/image-4292d818-bbb9-432f-8cf4-65ec951f93ab.png) ![image.png](/.attachments/image-45909d23-ffd6-45db-8b64-8c08c825d6cc.png)
 
###**2.6 Search Tips**
 ![image.png](/.attachments/image-0db5c4c9-ee6e-4c60-a0e1-da01cb4f13ea.png)
Clicking will open the Tip widget:
 ![image.png](/.attachments/image-24c99a27-7117-4d65-8113-7981b8cb3685.png)

##**3.0 Search Results Page (SERP)**
 ![image.png](/.attachments/image-7033598c-f21f-4ba8-9889-a653e372c6d5.png)
###**3.1 Main Search Component – (Reuse 2.1 Search Bar Unit)**
 ![image.png](/.attachments/image-a50534c7-8183-491a-9ada-0477e6f50860.png)
###**3.2 Tabs**
The results are distributed across tabs, along with the amount of results found in each one.
-	All
-	Entities
-	Documents
-	Multimedia
-	Data models
-	Map (Phase 2)
-	Favorites (phase 2)
####**3.2.1 All**
 ![image.png](/.attachments/image-76fb3c18-633d-4719-a301-dc00b01f7e6f.png)
####**3.2.2 Multimedia**
Shows all multimedia files found in the search.
![image.png](/.attachments/image-20dff1c8-ca3a-45f1-8cf7-879f6397dba1.png)
 
###**3.3 Facets**
  ![image.png](/.attachments/image-2fb8cd46-9a2d-4a58-bcf3-6e4a13f27ebb.png)Facet closed state
 ![image.png](/.attachments/image-26116e00-d169-4dd9-878e-fc9bfd1ed51d.png)Facet open state
####**3.3.1 Default behavior**
Read more in: [Facets (In Federated Search)](/TA9-WIKI/UX-UI/Facets-\(In-Federated-Search\)) 


####**3.3.2 Sorting**
 ![image.png](/.attachments/image-a7e1078c-dc61-42cc-92c2-cfdfda0507a5.png) High-Low – Default
 ![image.png](/.attachments/image-8e37de6a-dd46-4977-850e-c4e0894a5e18.png)Low-High
![image.png](/.attachments/image-83a0cad9-1f12-45e6-b815-6ea6e6784fe7.png) A-Z
 ![image.png](/.attachments/image-f595da6f-e043-47fb-ab52-086e0e182361.png)Z-A

####**3.3.3 See All (More Options)**
Each facet will have a "More Options" button opening the facets in a modal, allowing the following actions:
![image.png](/.attachments/image-7541366c-cd44-4e44-bfdb-6ba61280b4ad.png)
![image.png](/.attachments/image-586f1c0c-7c9a-45e3-84e3-dd5fdc1f476c.png)
1. Multi choice - Choosing several facets to filter on:
![image.png](/.attachments/image-37919f0b-796f-4942-b0e0-435bf97fac67.png)
2. Search for facet by textual input
![image.png](/.attachments/image-b9b8699a-3b14-4f61-a17a-d1446ea0cd9b.png)
 

###**3.4 Send To Widget (Quick Search)**
![image.png](/.attachments/image-b1bd1afa-ac69-4c2d-aa45-7b92608fb2ac.png)
Send the Query to a new search in an other Data Model / Sensor. 
Each Button has an icon + Text. Size is dynamic according to length.

###3.5 Result 
There are 4 types of results:
-	Entity (With/without an image)
![image.png](/.attachments/image-dca88dca-8553-4fd4-b0f1-ac15d4727c0e.png)
![image.png](/.attachments/image-3f87ff2c-7328-4f8d-9ec8-ec24dafb79f0.png)
-	Document
![image.png](/.attachments/image-8767cf31-4fc3-4d95-8f29-a635610b72e4.png)
![image.png](/.attachments/image-610581e3-ee87-4aba-ab45-cd60350c4add.png)
-	Multimedia
![image.png](/.attachments/image-0340abfb-560a-44f9-9357-c0923c958a49.png)
-	Data Model
![image.png](/.attachments/image-d709704e-148b-44b8-ae09-4f12e3d0f008.png)

###**3.6 Viewers** 
Viewers present the data found in the database of the result.
-	Fixed Width – 5 columns on a 12 column grid
![image.png](/.attachments/image-ffdd8df9-6551-4bc9-a5f3-4086af32cd92.png)
-	Anchored the right side of the screen, freezes on scrolling
---
#### **3.6.1 Viewer types**
There are 6 types of viewers:
- Entity
- Data Model
- Document
- Audio
- Video
- Image

##### 3.6.1.1 Entity Previewer 
 ![image.png](/.attachments/image-26339722-7280-4c49-8824-f6f62f06e5d0.png)
**Header Tabs:**
-	Preview – Default
-	Link Analysis
-	Annotation (Messages)

**Entity Tabs:**
 ![image.png](/.attachments/image-041857f1-cdfe-44af-8555-c48388fb0727.png)
According to the entities data card

Mark - ![image.png](/.attachments/image-9904b6ff-a1c4-4974-9f86-cae4201577e4.png)  / On - ![image.png](/.attachments/image-7ad5f2cf-fcea-4e05-9d5d-c1ebe1ebeb51.png)  

To Open the entity card in a new tab:
 ![image.png](/.attachments/image-bd00d2b8-af8b-4f8e-b5dd-ed367f044e3f.png) 

If there are several images to an entity – use a gallery. If not – don’t show galley buttons:
![image.png](/.attachments/image-12ec3203-ea2d-4e86-8ecd-a3af549e0b6a.png)  

 Data – If there are more than 14 rows – Present a “show more” button that will do the same as “Open” button mentioned above. 
![image.png](/.attachments/image-07dfec48-87ad-43b3-a4d0-4d2b27cb2da4.png)
![image.png](/.attachments/image-24f2a84b-2366-447a-8837-27c1bcd31f94.png)- Entity Tags. 

---
##### 3.6.1.2 Data Model Previewer 
![image.png](/.attachments/image-83ccc0b6-ebd6-4763-9c7a-0c8e97e359a2.png)

Header Tabs:
- Preview = Grid 
- Annotation (Messages)
- Map
- Link Analysis

Default skin will be the same as the Data model definition.

---
##### 3.6.1.3 Document Previewer 
 ![image.png](/.attachments/image-dfbf0693-bfee-457c-a250-221ed8c7b6ef.png)
Header Tabs:
-	Preview – Default
-	Link Analysis
-	Annotation (Messages)


Buttons :
- Open (Opens the Document viewer app)
- Translate – TBD (Simply create the UI)

---
##### 3.6.1.4 Audio Previewer 
![image.png](/.attachments/image-c455d95c-e2c9-4d98-ab11-c121fffafe11.png)

---
##### 3.6.1.5 Video Previewer 

![image.png](/.attachments/image-70a8b527-e0aa-4cdb-9e9c-794b4151de6d.png)

---
##### 3.6.1.6 Image Previewer
 ![image.png](/.attachments/image-46a7ba1e-534e-4340-b6e5-a6ddb6c16323.png)

---
#### **3.6.2 Viewer sections layout**
Each viewer will be built from 4 major components:
1. **Header / Tabs** - Main navigation between different displays
2. **Content Previewer** - Displays the content
3. **Metadata** - Provides metadata information on a file
4. **Tags** - Displays the tags created on the object
![image.png](/.attachments/image-17564d76-de54-428b-a371-05aef3a8112a.png)

##### 3.6.2.1 Header / Tabs
![image.png](/.attachments/image-6721c737-ec79-4c98-9910-27780d8b5ab6.png)In the header, we will present between 2-4 tabs, according to the data nature.
Tabs from left to right:
- Preview - Gives a preview of the object
- Annotation - Presenting comments made on this object
- Link analysis skin If configured on the data
- Map skin if configured
- X Closes the viewer

Each Tab has 2 states:
- Selected - opacity = 100% 
- Not Selected - opacity = 20%

Tabs will be aligned to the center of each column in the grid:
![image.png](/.attachments/image-f5d34b95-6d5a-459f-abf5-6aea6032c63e.png)

**Note! present only available tabs.** In case Link analysis/map skins are not available, the should not be presented:
![image.png](/.attachments/image-6f22619d-721c-404d-95cd-34015546e5c9.png)

###### 3.6.2.1.1 Annotations view
TBD
###### 3.6.2.1.2 Link Analysis Skin view (For Data Models Only)
![image.png](/.attachments/image-4c9ad57d-45ea-407d-9107-a0f1e0b52a06.png)
Clicking "Open" will open the data model, with the search criteria, in Link analysis skin.
###### 3.6.2.1.3 Map Skin view (For Data Models Only)
![image.png](/.attachments/image-54beecea-8506-47e7-9896-693c94a64c54.png) 

---
##### 3.6.2.2 Metadata 
The metadata displays extracted info:
1. Filename + extension
2. Date
3. Time
4. Location
5. Owner
6. Type and size

Each field in the above should be aligned to the grid columns:
![image.png](/.attachments/image-f65e0a5e-0458-422d-8b0f-5c03019beb25.png)

---
##### 3.6.2.3 Tags
In the Tags section, the system will present the given tags for the object.
The tags width will be aligned to the grid:
![image.png](/.attachments/image-1bc7dc4c-ab4b-4190-8deb-19f339415f23.png)

--- 
###**3.7 Combo Box**
Allows actions for each results:
![image.png](/.attachments/image-e46a94c6-bcd8-46c5-b58c-7ae98cb65a3f.png) Opens the combo box
 ![image.png](/.attachments/image-a37c085c-3a33-4ca8-a496-99fada7510c0.png)

---
###**3.8 Footer**
![image.png](/.attachments/image-d8e805bd-7cb7-4cc7-8a2f-558947ee776f.png)
Results per page – shows the results number the user wants on screen:
20, 50, 100

---
###**4 Actions**
####**4.1 Send multiple entities to Graph**
1. User can send multiple entities to the main graph by clicking the check button to check all, or manually select single entities:
2. The send to graph quick action will be displayed.

####**4.2 Send multiple entities to Map**
1. User can send multiple entities to the main map by clicking the check button to check all, or manually select single entities:
2. Send to map quick action will be displayed
![image.png](/.attachments/image-752302fe-ccfd-4ae2-9040-57842b49db23.png)

* Only entities that has a location value, will be sent to the graph
** An entity with location, will get an indicator next to the entity type, marking this specific entity has a location.
![image.png](/.attachments/image-0a53c270-dc23-40ae-86cf-1c9ec1a6cff6.png)

