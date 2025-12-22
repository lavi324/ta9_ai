 In IntSight V3.9 a new Link analysis skin capability was added - Link templates. This ability allows defining several "templates" of links in a data model, allowing the user to switch between the templates from the Web interface when each template can hold different links.

In this ability, a "Default template" property was defined, to determine what is the basic default set of links that will be seen when opening the data model skin.

When moving from older versions to 3.9 (upgrade) the support must take into account that there are currently links already defined in the environment we are upgrading, therefor the support team must run the following "_LinkAnalysistScript_" script, in order to make the current links be the "**default template**":

**LinkAnalysistScript description** -  An SQL script that creates "_default templates_" for each data model in the datamodellinks table and adds the "_template ID_" to the relevant links in the datamodellinks table. 

# Execute
To execute the script, make sure that:
1. The tables datamodellinkstemplates and datamodellinks exist.
2. There is the TemplateID column in the datamodellinks table.


**The Script:**
Run this to create this procedure
```
DELIMITER //
CREATE PROCEDURE LinkAnalysisScript()
BEGIN
set @DMId = 0;
set @Template = 0;
set @counter = 0;
set @Max = 0;
select Count(distinct(datamodelid)) From datamodellinks into @Max;
While @counter<@Max 
DO
	prepare datamodellinks from "select distinct Datamodelid FROM sqlite_metadata.datamodellinks ORDER BY Datamodelid LIMIT ?,1 into @DMId ;";
	EXECUTE datamodellinks USING @counter ;

	insert into sqlite_metadata.datamodellinkstemplates(TemplateName, Description, IsValid, Isdefault, DataModelID)
	select distinct "Default","",1,1, @DMId ;
    
	select templateid from datamodellinkstemplates order by templateid desc limit 1 into @Template;
    
	update datamodellinks join datamodellinkstemplates
	set datamodellinks.TemplateID = datamodellinkstemplates.TemplateID
	where (datamodellinkstemplates.datamodelid = datamodellinks.datamodelid and datamodellinkstemplates.templateid = @Template) ;
    
	select @counter + 1 into @counter ; 

    END WHILE;    
End;
```
Run this to call and run the procedure :

`call  LinkAnalysisScript();`




# How To define a new link analysis template 


## 1. Creating a new template

- Run the query `SELECT * FROM sqlite_metadata.datamodellinkstemplates;`
- Add a new row into this table with the template name and the relevant data model.

![image.png](/.attachments/image-14074a93-ea2c-4fcc-b773-e535af89c092.png)

## 2. Define the relations that will appear template
- Run the query `SELECT * FROM sqlite_metadata.datamodellinks;
- Add rows with the relations and with this templateID.

![image.png](/.attachments/image-316fd02a-ae61-42e4-9638-79d99eb481b3.png)