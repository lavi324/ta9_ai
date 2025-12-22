This Chapter review the Facets behavior, in the Federated search module:
Mockup: 
https://xd.adobe.com/view/b5436904-572a-4ef0-b604-c54363ed1c97-e010/

---
[[_TOC_]]

---
##**System Facet Types**
TA9 system should be preconfigured to support the following Facet types by default:

###**All tab**
1. Type - Data type (entities, documents, images, etc.)
2. Tags
3. Location - Display results by location (main long / lat), or based on EE - Add the value of **"Unknown"** in case the results don't have any location
4. Language - in case an extracted language is detected - Add the value of **"Unknown"** in case the results don't have any language detected
5. Data source - Filter based on the upload source
6. cases - Filter by case, Add the value of **"None"** in case the results don't have any case detected 

###**Entities tab**
1. Type - e/g entity type
2. Tags
3. Location
4. Cases

###**Documents tab**
1. Type e/g document type
2. Tags
3. location
4. Language
5. Data source
6. Cases

###**Multimedia tab**
1. Type - e/g file type
2. Tags
3. location
4. Data source
5. Cases
6. Object type - Appears when there's information on the type of objects within an image. For example Car, Van, Person, Plane, Bicycle etc. Most likely to have this information on enriched data - extracted by cloud services like Azure.
7. Entities - Appears in an entity face in an image/video match the entity face in the system (based on Face recognition service)

###**Data model tab**
1. type - e/g DM type
2. Location
3. Data source
4. Cases
5. Range - filter the results according to a range of results
6. Tags


--- 

##**Default State On SERP**
- When the Federated search results page opens, It will display the Facets Sidebar opened by default. 

- The user will be able to close the facets bar by clicking the following icon:
-- Open State![image.png](/.attachments/image-2887751f-0bbb-4276-b8b8-696bc7ea9c91.png)
-- Closed State![image.png](/.attachments/image-66fd09d4-a749-4eaa-8159-60fdafb9ef05.png)

---
##**Default State In Facets bar**

- Each Facet will have a "Collapse" button, allowing the user to toggle between 2 display states.

- The Default view will be an "open" state for all facets.
-- Opened ![image.png](/.attachments/image-7541366c-cd44-4e44-bfdb-6ba61280b4ad.png)
-- Collapsed ![image.png](/.attachments/image-6c8be479-f349-4c97-9d09-12beee7e062a.png) 
_notice that in the collapsed state we don't see the sorting buttons._

--- 
##**Displaying Facet type - Results**  

- Each Facet will Display the same number of result types by the same Fixed Value **"X"** when in "opened" state. 

- Total Amount of results will appear in the Main title next to the "type definition" in brackets 
![image.png](/.attachments/image-0c3f3c4e-b08a-4a89-a26b-d0a96118806e.png)

- The results fixed value **(X)** can be defined by changing the configuration from the "config" tool.

- When a number of results type is larger than **"X"**, they will appear in the "More Options" modal:
-- Top: Showing <x
-- Bottom: Showing >x
![image.png](/.attachments/image-95e4d4bd-55d2-4ec4-af00-16dce960e971.png)

- In case the number of selected facets is bigger than the "Fixed Value" configuration, the UI should display all selected facets

---
##**Filtering**
- "All" filtering is selected by default and will be the first in every list.
![image.png](/.attachments/image-f74c68ff-892c-4462-89cc-898182e945cf.png)

- Clicking on other filters, will deselect "All", and select the other
![image.png](/.attachments/image-af5a856d-4b4b-4a9b-aab3-a70bceda6da7.png)
Notice that the "All" now inherits the sum we have in all displayed facets

- Clicking again on the selected type will deselect it, and run the query again without a selection. 
Also possible - to click on the "all" to cancel the filter to run the query again.

- To Choose several filtering options (MultiChoice) the user will click on "More Options"

---
##**Sorting**

- The Default sorting will by descending by count

- The user can change sorting to by ascending, A-Z, Z-A
-- Descending ![image.png](/.attachments/image-f6cd385a-2d42-48a9-aa9e-f962c9cad3c0.png)
-- Ascending ![image.png](/.attachments/image-ab32e1eb-ed22-4096-8a47-277472b5bb4b.png)
-- A-Z ![image.png](/.attachments/image-e8e7fd75-7918-4979-bc5b-25b2686fff2d.png)
-- Z-A ![image.png](/.attachments/image-17bb35b6-7f40-4454-98cb-2c195894b910.png)
*Each sorting state replaces the previous one, Icon and results changes accordingly 
*"All" should remain the first option no matter what is the sorting state, and always appear (even after choosing a filter)

--- 
##**Clear All Filters**

- In order to restart the Facet filtering, the user will be able to click "Clear All" to go back to the initial state.
![image.png](/.attachments/image-d5233d09-52dc-4673-aa1c-88a5b19b3e04.png)

- "Clear all" will only be visible when a modification in the facest had been done

- Clicking the clear all will run a new query based on the main criteria (+ Advanced)

---
##**Scrolling**

- Facets bar height should spread out on maximum height
![image.png](/.attachments/image-2cc7ba6a-50cf-43e4-8908-aa912c133059.png)

- When scrolling, the Facets bar stays fixed, and scrolls down/up with the screen
![image.png](/.attachments/image-e23c0e98-89ac-4a9d-9539-28a6c521c912.png)

- In case the facets bar content is too long, allow an inner scroll within the facets bar. 

- The Inner scroll should be invisible

--- 
##**More Options Modal**

- The modal (once clicked) will Show the user all available facets

- Allow the user to use MultiChoice selection

- Inherit the same sorting state from the Facets bar

- The first value in every list will be "Select all". Clicking it will select all facets in the list.
![image.png](/.attachments/image-8e84f980-6084-4452-bdbd-4751e7e5c1e2.png)

- Re-clicking on "select all" will deselect all facets
![image.png](/.attachments/image-c3d57c81-cd3b-4680-8479-1ba48669a2ad.png)

- Clicking on any facet, simply removes/add it from the current selection, removing the "Select all" if clicked:
![image.png](/.attachments/image-76bb6a5d-9d58-436a-8d79-9f1f1c7e0ffd.png)

- The footer displays the number of Filters chosen:
![image.png](/.attachments/image-fd77b511-5687-44a9-849d-dfa512a4826f.png)

- To run and approve the filtering - The user will click "Apply"

- To cancel the filter - the user will click on "X"

- The search will be used to display relevant results according to the input, Filtering the categories while typing:
![image.png](/.attachments/image-b9b8699a-3b14-4f61-a17a-d1446ea0cd9b.png)

- In case the facet list is long - a scroll will be possible. keeping the header and other in place:
![image.png](/.attachments/image-f95016e3-307c-4075-a487-84277ac8fc76.png)

--- 
##**General comments**

- After each query/filter, the facet list will refresh, and will display the new facets retrieved from the server according to the returned results.

- For Future purposes, keep in mind the facets bar may hold different UI components, and not only checkboxes (like Range, Color etc.)

- TBD - In the next design phase, the facets modal will allow browsing between different facets types. Example design:
![image.png](/.attachments/image-98b14e72-62d2-4e0a-87d6-9ce9b177364e.png)