# Environments without internet access : 
1. In system_config table, the value in 'geoCodingProviderName' needs to be 'Custom'.

![image.png](/.attachments/image-3cf53239-a197-4997-8042-7f5052fca126.png)

2. In endpoints_manager table, the value in GeocodeServerUrl needs to be 'http://X/nominatim/search'                                                                                                              *Change the X to the server name

# In environments with internet access : 
1. In system_config table, the value in 'geoCodingProviderName' needs to be NULL.
2. Open on the server the configuration file 'ol-geocoder.js' located in this path:                                    C:\Program Files\TA9\Web\Web Client\app\content\vendor\openlayers\ol_ext\ol-geocoder
3. Search for this URL: https://nominatim.openstreetmap.org/search
If the URL is:https://nominatim.openstreetmap.org/search/ ​remove the / save the file
4. Restart the ta9 in the IIS and clear the cache
