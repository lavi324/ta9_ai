## General
Dependency Roles are a way of configuring entity form behavior based on entity's values. For example, hide a field based on other field's value (let's say, don't display 'Death Date' field only if 'Is Dead' checkbox is set to true).

## Dependency Roles Types
There 4 types of dependency roles:
1. **Visibility**	The visibility of a property can be depended on another property value. For instance: Only if the property "Has Kids"=TRUE then the property of "Kid Name" will be relevant and will be visible.
2. **Validity**	A property value can be depended on a rule in order to determine its validity. For instance: The property "Age" should have a validity check that its value is greater than zero.
3. **Behavior**	The behavior of a property (such as a lookup list) can be depended on another property value. For instance: Only if the property "Country"="USA" then the lookup of property "City" will contain only the cities of USA.
The configure in that case will be as following in the 'em_dependency_roles' table:
![image.png](/.attachments/image-2467af43-e71a-4e6e-990a-ef32d0d1e28d.png)
Where:
- Id=11 is auto generated
- DependencyRoleTypeID=3 is the type id of Behavior
- PropertyDefinitionID=770 is the field id of the City field
- ParentPropertyDefinitionID=771 is the field id of the Country field

The 'lookupmanager' table specifies the fields by which the child table and parent table are connected (Similar to how SQL JOIN works).
![image.png](/.attachments/image-294fc643-b401-47ab-81e9-ea043275fb60.png)

Parent - country table:
![image.png](/.attachments/image-53a11541-78ff-47ff-ba71-51af1bdc6722.png)
The 'iso3' column is the connecting key for the child table.

Child - cities table:
![image.png](/.attachments/image-bba39b30-bede-446c-927f-abf666b6d54f.png) 
The 'Country'ISO' column is the connection for the parent table.

4. **Parent-Child**
this type of role uses to **automaticly fill relevant data** for the child fields  
4.1 **ParentLookup**	The parent from parent-child lookup
"lookup" field based on the federated autocomplete,
corrently support only Data models that had been indexed to federated
4.2 **ChildLookup**	The child from parent-child lookup
actually it will have only one value - not list of values like lookup.
it will automatically fill the data from the chosen row 

**For example:**
In entity  "event" we want to have the event data, and also the data about the person related to the event - id , name, address.
also, we have DM "citizens" with data about all people in the country (and this DM is indexed to the federated)
in our case, in event DM we will define:
- "ID" field will be **parent lookup**:  
 will give us autocomplete on all citizens data - and will hold the "id" we will choose
- "name" and "address" field will be **childs lookup**:
once we choose value for the "ID" it will automaticly fill the value for the relevant "name" and "address" by the chosen ID

## Notes:
1. Currently, 'Behavior' type is used only for Lookup Parent Child (filter lookup like country -> city)
2. DM Parent Child isn't available via Admin console, see #37038. So Only configure on DB in table "em_dependency_roles" in schema "sqlite_metadata", for example:
![image.png](/.attachments/image-b08f5251-e442-4676-9148-3f49af2d6fb1.png)

DepandencyRoleTypeID - from the "em_dependency_role_types" table (4 - for ParentLookup, 5 - for ChildLookup)
PropertyDefinitionID - The entity property ID, Parent
ParentPropertyDefinitionID - The Parent entity property ID
OperatorID - can stay NULL
Value - The DM ID
RelevantFieldName - The field name
SourceType - 2 = entity, 8 = data model

The entity property ID 491 is the parent of the entity properties ID 482 and 484. ("em_property_definitions" table)
Each time the user will enter a value in the property with the ID 491, it will look on the DM with the ID 379, on the field name 'Column1'.
It will fill up the child properties ID 482 and 484 with the values from the same DM 379 and same DM row according to the field names 'Column2' & 'yevuan'.

## 5. **Entities AutoComplete lookup field**

in case you need to define lookup field base on autocomplete - we define it similar to the "parent lookup" -
* dependencyToleTypeID = 4 (Parent lookup)
* property definition id = the id of the property that should be entities lookup
* value = the entity ID (the entity we want the lookup to look at)
* Source type = 2 (2 = entity, 8 = data model)

for example:
![image.png](/.attachments/image-9923611f-51d5-4f3c-bb13-9b3b38e2eaf1.png)

with this definition - when we open entity X that have property 1476,
this property will be autocomplete lookup on entity EN15
the lookup is working on "display title" field