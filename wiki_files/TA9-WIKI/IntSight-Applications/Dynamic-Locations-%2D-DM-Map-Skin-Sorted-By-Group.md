# **Feature Description:**
Allow displaying on a map view a relative location of "main longitude" and "Main Latitude" to a predefined "display title".
Meaning - Using the "group name" property as a "Display title", for location values.

## **Participating properties:**
In the Data model definition screen from the Admin Studio:
- Group name - representing the link between the display title value, and the location values
- Main display title role - Applying this field as the main display title when we have more than 1 location to represent
- Main Long/Lat - represent the longitude and latitude fields + adding a group name to identify to which Main display title they will be assigned.

Pre-conditions:
- Having a data model that contains 2 different sets of long/lat, both defined as "main" and the wanted display titles. In this example, we address the CDR data model, with 2 sides of the conversation as '**callFrom**' (appelant) and the latter '**callTo**' (Appele).

![image.png](/.attachments/image-01f341c0-68dc-4b88-bf34-c7e0411dc916.png)


# ***Troubleshooting***
The location presented on the map sometimes displays the number of the other side of the call. Meaning - the phone number that was presented in the title of the location in the map, was of the person who made the call, while the location displayed is of the person who answered the call, and vice versa.

For example:

![image.png](/.attachments/image-57a76551-d654-4ec7-a1c3-3ac9e22c4b69.png)

The location is of the 'callto', and the displayed title is of the 'callFrom'.

-----
# ***Solution***
we are connecting a value found on each side of the call to it's relative location (main longitude and latitude) by creating groups, for example:
_GroupName = 'To' {Conatins the fields 'appele', 'longitude appele', 'latitude appele'}_
In this way, they are presented together on the map skin.

In order to display the right location and phone number together, we can follow the next steps in the Admin Studio:

## **1. Go to DM settings:**

![image.png](/.attachments/image-efbbbba4-a001-46db-abe8-8a3801c31fd7.png)
![image.png](/.attachments/image-17027351-4eba-4bc7-b252-b376b0f5afd0.png)

choose CDR DM:

![image.png](/.attachments/image-e22c7cdf-e897-4348-aec5-7dd633036a67.png)

## **2. Set the following specifications:**

2.1 In the column  "From" Set:
- Group Name: "From"  
- Field Role: "Main Display Title"
![image.png](/.attachments/image-b8ac1fdb-6a93-4c4f-ab37-61f885f954f9.png)
![image.png](/.attachments/image-e0f7a8a1-3bf6-4aa1-9607-4a4adcd67e45.png)

2.2 In the column "Longitude From" set:
- Group Name: "From" 
- Field Role: "Main Longitude"
![image.png](/.attachments/image-ad3d806f-45bb-434e-9767-dd4971c7756e.png)
![image.png](/.attachments/image-1d1c6193-3d41-4607-831d-ed70a42b26d1.png)

2.3 In the column "Latitude From" set:
- Group Name: "From" 
- Field Role: "Main Latitude"  


2.4 Repete the process for the second group of locations with group name "to"

-----
Now you can clear the cache (server & client) check and see in the CDR DM on the map skin, that the display title matches the location specified on the map:
![image.png](/.attachments/image-e7c88a33-be69-4ac4-8390-606df327f269.png)


