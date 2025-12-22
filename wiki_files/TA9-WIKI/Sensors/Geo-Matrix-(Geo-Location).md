[[_TOC_]]

# Intro
GeoMTRX is a sensor (owned by _RayzoneGroup_) that can be used to **locate** a phone number.

The product is SaaS and can be used only via URL (not on-prem):
- Production: https://geo.mtr-x.com/
- Staging: https://geo.mtr-x.com/staging/

![image.png](/.attachments/image-596876ba-bf9c-49f4-a821-7b8a7de99bcc.png)

# TA9 Integration
When fully integrated, the following capabilities achieved:
1. Users are synced between systems
1. Sensor is opened from within _IntSight_ with SSO
1. Entities are synced into _GeoMTRX_ (only those with Phone Number identifier)
1. Data is collected from _GeoMTRX_ into _IntSight_ (configurable) 
1. Historic data can be analyzed using a data-model
5.1. The _'Historic Data'_ is actually location-queries that were performed by this organization/user on _GeoMatrix_ and it can be analyzed (e.g - all locations of a specific target [identified by phone-number] can be shown and investigated)


## Load Data
Geo Matrix historic data can be loaded into _IntSight_ using 2 ways (**usually only 1 is used!**):
1. **Files Loading** - using _IntSight_ Auto/Manual Loader, exports from _GeoMTRX_ can be loaded to the system.
This method is usually used on offline environments or when the client don't wan't ongoing sync of historic data, but only on-demand.
1.1. Parser - use _"Geo Location Parser (MTRX)"_
1.2. Sample file -  [Geo_data_sample.csv](/.attachments/dasGeo%20data%20satew-7a4e6b22-1ed7-4965-8c7a-89131ab8be52.csv)
1. **Polling** - IntSight can poll GeoMatrix for new data every X seconds and save it to the Location History DM (no manual loading is required)



# Integration Guide
1. Run the script `Argus/DBScripts/MySql/AdditionalScripts/ta9_apps_geoLocation.sql`
1.1. Pre-configure the script with `DEV/PROD` URLs
1.2. Pre-configure the script with _GeoMTRX_'s Admin user & password (get it from Geo)
1. Restart `TA Host Service` & At this point users-sync & DM should be working
1. **Data Loading**
3.1. Install _parser_ from `Utils/Parsers/Parsers/GeoLocationParsers/GeoLocationParsers.MTRX`
3.2. The following files should be on _parsers_ folder:
![image.png](/.attachments/image-1febf676-91a3-40d7-b516-a0eaf4175080.png)
3.3. Now, data can be loaded to the system using Manual or Auto-Loader, specifying the right parser (see sample above)
3.4 **Note:** Finish the geo matrix tutorial after the first activation of the app.
4. **Automatic Data Polling**
4.1. This can be configured by configuring our service to do polling from _Geo service_
4.2. Goto `Sensors.Service` and open `Sensors.Service.dll.config`
4.3. Set app-setting key `IsPoller` to `true`
4.4. **Notes**
4.4.1 Set this config to only **ONE** instance on environment
4.4.2 _Polling_ is done with `ServiceAdmin`'s connected user (`usersensors where sensorid=1 AND usersid=2`)

## Integration Checklist
1. Location History DM id must be = 108 (otherwise must be changed on config `geoLocationDM`)
1. _Geo Matrix_ sensor id MUST be = 1
1. Users that has the _GeoMatrix_ sensor permission are regularly synced to _Geo_ system

## Test the integration (sanity)
1. With admin user (`userid=1`), locate the '_Geo Matrix_' App and click the tile
1.1 **Expected**: _GeoMatrix_ web-access client should be opened already logged in
1. With the `admin` user (`userid=1`) open the _Admin Studio_
2.1 Goto _Users_ and choose a user (or create one)
2.2 Check the _GeoMatrix_ permission App
2.3 Login to _IntSight_ with that user
2.4 locate the '_Geo Matrix_' App and click the tile
2.5 **Expected**: _GeoMatrix_ web-access client should be opened already logged in
1. **Data Loading**
3.1 Goto IntSight load screen
3.2 Choose the sample file mentioned above
3.3 Choose Type: _'Data Model', 'Location History'_,  Parser: _'Geo Location Parser (MTRX)'_ & Load
3.4 **Expected**: All rows from within the file should be loaded and accessible from _'Location History'_ DM
1. **Polling (only if configured)**
4.1 Goto _GeoMatrix_ app & perform sample query (starting with 999)
4.2 Wait a while (max by config `PollingInterval`)
4.3 **Expected**: The location-query should appear on _Location History_ DM


# Additional Sensor Notes
1. Users are divided into departments. Each department has its own restrictions regarding countries that can be located
1. When want to test, always use a number starting with 999, e.g **999**12345678


# Troubleshoot

Message: Failed getting the value of the key 'geoLocationDM' of module 'Net_SensorsService' from the config service.

make sure that on MySQL this configuration is set: 

SELECT * FROM sqlite_metadata.system_config;

![image.png](/.attachments/image-f91eb197-85e2-4a86-9a6a-7f79a4cc578e.png)

and :

SELECT * FROM sqlite_metadata.system_modules; 

![image.png](/.attachments/image-224543f9-6c0d-4cb9-aa20-b37f21f208e3.png)


to check the configuration : 

http://XXX.XXX.XXX.XXX/#/admin/configurations

![image.png](/.attachments/image-9396ac38-5e4d-4748-9c7d-40ee9724cd3b.png)


____________________________________

# Isuzu
Sensor id = 1
Sensor Name = Live Location

# Scenario:
User with permission cant login to the live location app
Error Code 2037

![image.png](/.attachments/image-d3c74690-c80f-4b17-b7d5-98f1e86f6288.png)

# Resolution: 

1. Open MySQL Workbench
2. SELECT * FROM sqlite_metadata.usersensors where sensorid =1 and isActive=1 and sensorPassword is null;

Validate he has permission access to it.
get user id from : 
SELECT * FROM sqlite_metadata.users;

sensorUserName = as the user name for the webapp without the AD 

for exemple: 
kkonan@evoir.local = kkonan in geo app

And sensorPassword should be Geo12345

You can see the users list in:

[https://geo.mtr-x.com/v2/main/]()
User Name:
ivcint.admin
Pass:
Geo123



