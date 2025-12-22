The changes made in Isuzu prod:



**Schemas**:
* _identifierstype:_
field: image URL - metadata/identifiers/10.png

* _dataschemafield1:_
   1. field: additional parameters: custom path from system config 
   2. In field AdditionalParameters add the URL to the folder on each viewer column (addition to custom path configuration).

* _sensors_: 
SensorURL - URL 3.9 to URL 4.2

* _system congif:_

   1. In config key _SapLoadBulkReadFolder_, changed the config value to _/sap/upload_.
   2. Add Zip value to _InternalWhiteListSupportedFiles_


*  _Data Loader table_
Autoloader setup

* _dataschema1_
DM image URL.


**General Changes:**
1. Changed page size for the following data models
- Hora data
-  Hora
-  Hora Summary

2. The largefiles configuration is
_/tmp/largefiles_

3. orient db settings in _dataconnectionsmanager_ table

4. orient db: 
_alter database custom standardElementConstraints=false_






