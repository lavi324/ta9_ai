
[[_TOC_]]


# Data table 
Each data model is based on a data table, the data tables can exist in MySQL / IQ / Oracel / Hive and must be created before creating the data model.

# dataschema1
For each data model, there is a row in the ‘dataschema1‘ MySQL table. 

**Check these columns while copying:**
- [ ] SchemaID – ID of the data model. Make sure the ID does not exist already in this table.

- [ ] DBTableName – The name of the data table the data model is based on. 

- [ ] ConnectionID – ID of a row in table ‘dataconnectionmanager’ that includes the Connection credentials for 
the database where the data table exists.

- [ ] DBSchemaName – The schema name of the data table where the data table exists (Not required if this exists in the connection ID).

# dataschemafields1
All the fields in the data models are defined in this table.

**Check these columns while copying:**

- [ ] SchemaID - should be the same ID of the data model that appears in table dataschema1. 

- [ ] FieldID – Auto increment ID. Make sure to nullify this field, since is an incremental auto-generated field.

- [ ] DataEnrichmentName – Lookup name. when there is a lookup that is set on this column.  Make sure the lookup exists in your environment (In table ‘Lookupmanager’).

- [ ] IdentifierTypeID - identifier ID. when there is an identifier that is set on this column. Make sure the identifier exists in your environment (In table 'identifiertypes').

# datamodelgrouphierarchy1
In this table, we define the data model to appear in a folder or in the main window. 

**Check these columns while copying:**
- [ ] ObjectID - This field corresponds with the data model’s ‘SchemaID’.

- [ ] FatherID – This field shows if the data model exists in a folder or in the main window. Main window = -1, another number means a folder ID (Make sure the folder ID exist in your environment in table ‘datamodelgroup’).

# userdatamodels1
In this table, we give permission for users to see the data model.

**Check these columns while copying:**
- [ ] ObjectID – This field corresponds with the data model’s ‘SchemaID’.

- [ ] userID - This field represents the user, check the ‘users’ table to translate the ID to the username.








