##Locate OpenLayers folder
The OpenLayers folder is located at the app folder common path to app:
C:\TA9\Web\app\content\vendor\openlayers\ol_ext\ol_geocoder

##Edit the js file
locate the ol-geocoder.js file and edit it with any text editor
![image.png](/.attachments/image-6b4c5da1-0ec5-4a1b-94a4-729a5cc9e474.png)

##Remove the unwanted /

Search in file the following text: https://nominatim.openstreetmap.org/search/
You will find only 1 match.
Remove the slash (/) at the end and the text should look like this: https://nominatim.openstreetmap.org/search

##Save and restart
Save the file and restart the site in the IIS

