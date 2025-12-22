# Update for limiting access for specific menu for admin users in Admin Studio

## 1. Added 3 new tables for tiles
_admin_studio_supported_tiles_ - All available tiles(menu)
![image.png](/.attachments/image-de798c62-f79f-4fd4-9beb-a6c74a7a796d.png)
_admin_studio_profile_supported_tiles_
![image.png](/.attachments/image-25fd4173-7003-44ef-848a-fbe84d22640c.png)
_admin_studio_user_profiles_
![image.png](/.attachments/image-b587292f-c85e-4304-915c-b31e907071ec.png)
2. _***If user does not have associated profile he will see all tiles**_
* If you want to limit access to tiles for specific **user** add new **profile** with tiles that user can access to **admin_studio_profile_supported_tiles**.
* Add new line to **admin_studio_user_profiles** with this **UserId** and **ProfileId** that you created or use previously created **Profile**.


