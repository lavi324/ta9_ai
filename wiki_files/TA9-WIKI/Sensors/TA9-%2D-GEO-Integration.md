[[_TOC_]]

# Intro
This documentation describes the TA9-GEO integration. Updated to September 2025, and applicable with at least the following versions:

- TA9 4.5.1 Official Version
- Geo Matrix `geo.mtr-x.com/v3` Version. (updated to September 2025)

> NOTES:
> - SSO is not supported
> - IP Address of application server must be pre-approved with Geo to access the service

---

# Updated 451 services
    - Sensor service: `ta9repo/ta9.intsight.sensors-service:4.5.1-333`
    - User management service: `ta9repo/ta9.intsight.usermanagement-service:4.5.1-379`
    - Admin gateway service: `ta9repo/ta9.intsight.gateway-admin:4.5.1-341`

---


# Configurations
## 1) sqlite_metadata.**usersensors** Configuration
In the sqlite_metadata.usersensors table, a row should exist for each TA9 user who wishes to use the TA9-GEO integration.
Each TA9 user configuration should include the following data in the table row.

- On column **userid** - insert the TA9 user id as seen in the sqlite_metadata.users table.
- On column **sensorid** - insert the GEO sensor ID as seen in the sqlite_metadata.sensors table
- On column **sensorUserName** - insert the GEO application user name - to be provided by GEO.
- On column **sensorPassword** - insert the GEO application password (for the user in sensorUserName column) - to be provided by GEO
- On column **IsActive**, set the value to 1
- On column **userSensorStatus**, set the value to 1
- On column **usersensorid** set the value to 1
- The columns sensorUserCreationDate, sensorUserLastUpdate, sensorLastLogin are not part of the integration and need to be filled with relevant dates manually. (They will not be updated automatically, and are not part of the integration). 

> **Password encryption** - the password for Geo sensor must be encrypted in the userssensors table.
To encrypt passwords - use a dedicated API provided with the latest usermanagement service:
ta9repo/ta9.intsight.usermanagement-service:4.5.1-379 - for documentation see below chapters.


## 2) sqlite_metadata.**sensors** Configuration

`In the sqlite_metadata.sensors table, at the row of the Geo Location app, the following configuration should be set.`

- On column SensorUrl - responsible for SSO login to the system - the following URL should be set: 
`https://geo.mtr-x.com/v3/?at=<APPTOKEN>#notarg`

- On column AcceleratorUrl - responsible for SSO and sending a number to Geo, the following URL should be set
`https://geo.mtr-x.com/v3/?at=<APPTOKEN>#notarg&a/service=locate&msisdn=[Phone]&tryLive=true`


## 3) Polling Flow and Configuration
The polling feature, if activated, polls data from Geo based on the queries users had run in GEO

In the sqlite_metadata.system_config table, the following ConfigKeys enable the availability and set of the polling configuration.

- **geoLocationPollingUploadFilesToFileServer = true** ConfigKey determines if the polling feature is active or not. look at that row on the ConfigValue column; if the word 'true' is written, it means that the polling feature is active.

- **GeoLocationIsPoller:** true

- **PollingInterval = 4000** ConfigKey determines the polling interval (in seconds), meaning the interval the TA9 sensor service tries to pull the data from GEO, based on the queries TA9 users sent to Geo. Internal period is set on this row on the ConfigValue column.

- Each interval time, the sensor service will search for queries that were run by TA9 users to the GEO app (from the last interval), and will send a request to GEO to get the query data and insert the data to the Location History Data Mode - ID 108.

- **sqlite metadata System_config** - geoLocationDM: 108, and with StateIDset to 1. 

- **GeoLocationQueryTime:** query_time


## 4) Sqlite metadata Endpoints manager

- **Endpoints_manager** GeoLocationQuery: `https://geo.mtr-x.com/api-prod`

## 5) Vault Secret
Secret name: GeoMatrix

    {
    "GeoMatrixApi": "https://geo.mtr-x.com/api-prod",
    "GeoMatrixVersion": 3,
    "GeoUserId": 1,
    "Limit": 1000,
    "StartTimeFormat": "yyyy-MM-ddTHH:mm:ss+0000",
    "UsePoller": true
    }

> NOTES
**GeoUserId** = should be the main admin user of the system - the permission for the sensor should be granted, meaning it should be in users_sensors - that this user has permission to geo app, including the password and user name.
>
> **Limit** = the max amount of results the poller will collect in each interval

---

## Location History Data model definition
[Location History Schema fields 1.csv](https://ta9comp.sharepoint.com/:x:/r/sites/ta9_share/Shared%20Documents/TA9%20Knowledge%20Base/Geo%20Integration/Location%20History%20Schema%20fields%201.csv?d=w5225bb78ed174adc93731af987e015c0&csf=1&web=1&e=wBGTXr)

[geomtrx data table.txt](https://ta9comp.sharepoint.com/:t:/r/sites/ta9_share/Shared%20Documents/TA9%20Knowledge%20Base/Geo%20Integration/geomtrx%20data%20table.txt?csf=1&web=1&e=UOqKaT)

>NOTE: Location history table should be on IQ
---

# Password Encryption API
Follow the steps to encrypt password for existing user
[Password encryption process](https://ta9comp.sharepoint.com/:f:/r/sites/ta9_share/Shared%20Documents/TA9%20Knowledge%20Base/Geo%20Integration/Password%20encryption%20process?csf=1&web=1&e=sPgtyC)









