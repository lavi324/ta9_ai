Each data model is different and the reasons for a failure in the upload can have 

The basic steps to understanding what causes the problem:

1. Check the user have permission to the data model and to upload files

2. Check if serviceadmin has permissions to this DM

3. Check you are able to upload all kinds of files to the system

4. Validate the mapping while uploading the DM

5. Try to upload just one column of the data model (text data type), and the required columns if there are any

*If 5 is succeeded* :
Upload the file, each time add another column until the file will fail, then you will know what column is dropping the file.
usually it is one of:
a - wrong date format
b - the text exceeded the limit of lenght defined for this column  

*If 5 is not succeeded* :
 
6. Make sure the data model is not defined as "Is Managed" in the Admin studio

7. In Admin Studio Validate all columns' "display field" are matching the columns names in the table created in the database itself.

8. make sure the table in the database have the default columns: departmentid , caseid, fileid (in **lowercase** (!!!) )
