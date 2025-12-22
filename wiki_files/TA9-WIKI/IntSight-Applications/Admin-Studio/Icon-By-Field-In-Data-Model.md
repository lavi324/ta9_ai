[[_TOC_]]

##Intro
We will explain how we can show different icons in the data model **map** skin.

##Loading The Icons
Upload icons to the filler and Upload the images to a folder under public/metadata 

![image.png](/.attachments/image-fe83ea8c-0ceb-4952-a5d9-3e3b2f1f2770.png)

##Creating Icons Lookup
First, we will create a table  for this lookup in the MySQL database:

![image.png](/.attachments/image-1429bb88-0269-4477-81a2-f3262a269b82.png)
We should have three columns:
**id** = icon lookup id
**value** = icon lookup value
**icon** = icon lookup, it will be the icon path
For example, If I uploaded the images to the path: public/metadata/dataproviders/
In the lookup, I add the value - **metadata/dataproviders/call.png**

Second, we will add the icons values to the lookup table:
![image.png](/.attachments/image-8b0d1f74-a08d-4d19-95de-92cdb828627b.png)

And now we can create the lookup from the 'Admin Tool'
1. Click on the 'Lookup Manager' tile
2. Click on the '+New' button
3. Select the 'MySQL' option, and add the data connection
4. Set the fields and save
![image.png](/.attachments/image-5bd6e3b5-3449-4076-be37-e25061f3c9c9.png)

##Data Model Icon Lookup Column
From the data model definitions page, set the Icon Column with the new lookup

![image.png](/.attachments/image-3b98f5c9-f4a9-443b-b89d-8d85f1131e12.png)

##Data Model Icon By Field Definition
Click on the 'Symbology Properties' button and select the 'Icon By Field' option. Now you just need to add the icon field and save.

![image.png](/.attachments/image-197aa876-0957-40d5-a9e5-9dff31777bec.png)

##Data Model Map Skin
In the data model map skin, each result will display with its defined icon

![image.png](/.attachments/image-93d17894-f83b-46da-af9b-327d0fb4b0d2.png)