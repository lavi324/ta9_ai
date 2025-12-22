[[_TOC_]]

##Intro
The Max Cluster Zoom Level is a definition for a Data Model with a location.

From the Admin Studio:
![image.png](/.attachments/image-fb9bffec-bda2-45ec-937c-4c2110611676.png)

##Max Cluster Zoom Level 
means that in case the current zoom level is higher items won't be clustered on the layer
Admin: Appear
Default Value: -1, items will be clustered always
Map Skin - Not enforced
Map Layer - Working
In case no cluster should be done, the max level should be set to zero

By defining the Max Cluster Zoom Level, for the data model layer and Map skin, in case the current zoom level is higher than the "Max Cluster Zoom Level" items won't be clustered on the layer and Map skin.

##Cluster Distance
From which distance between items in pixels the items should be clustered to each other

Admin: Appear
Default Value: 40, means items within a distance of 40 pixels will be clustered to each other
Map Skin - Working
Map Layer - Not enforced

##min_zoom_level
From which zoom level to present items. if the current zoom level is lower no items will be presented.

Admin: Doesn't appear, can be edit only from DB
Default Value: 0, means items always presented on default
Map Skin - Not enforced
Map Layer - Working 


More information in the ticket: https://dev.azure.com/ta-9/Argus/_workitems/edit/39598