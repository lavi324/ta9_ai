**Troubleshooting**

Entities can't be modified - couldn't update entities with existents data from Admin studio.

•	***The problem:***
Before you can understand the problem, you need to understand a few things:
1.	in general - when we changing entity definition, in order to make sure the user's changes wont influence the existing data - 
2.	we preform some checks to verify it.
3.	one of the checks - is to make sure that for existing properties - we do not change the type.
4.	somewhere in the Admin studio code - after every save tried to validate the entity definition, 
and in case there is some property with lookup - it automatically changes the type to TEXT.
5.	every entity gets the system fields when it gets created,
it gets the properties definition from the table : "em_system_property_definitions"
in there - we defined the fields "Sys_CreatedBy" and "Sys_LastUpdateBy" with lookup and with type "LONG" (number)

when you combine all these facets you get the following problem-
when you try to change entity definition, when the entity already has data - if it is the first time - it will try to also change the type of the properties "Sys_CreatedBy" and "Sys_LastUpdateBy" - and the system will fail this change.

•	***The solution:***
	**production solution:** 
1. in every exist entity, change the type of the fields **"Sys_CreatedBy"** and **"Sys_LastUpdateBy"** to text. Acordding to DataTypeID (text = 1 and long(number) = 4).
you need to do it inside the DB in table : **"em_property_definition"**. 
The query should be:

`UPDATE `sqlite_metadata`.`em_property_definitions` 
SET `DataTypeID` = '1' 
WHERE `DataTypeID` = '4'`

2. to make sure it will work for new entities in the future - change it also in the system table **"em_system_property_definitions"**.

**Product solution:**
change it in base script in "em_system_property_definitions"
 