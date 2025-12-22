This script allows To create a large amount of tasks and cases.

**For cases:**

```
delimiter //
CREATE PROCEDURE myproccase()
BEGIN
DECLARE i int DEFAULT 0;
DECLARE cases_amount int DEFAULT XXX;
DECLARE case_index int DEFAULT XXXX;
    WHILE (i <= cases_amount) DO
		INSERT INTO sqlite_metadata.investigationheader (InvestigationID, InvestigationName, InvestigationType,InvestigationSubType,StartDate,LastUpDate,CreatedBy,IsActive,Status,Mode,GroupID,SubGroupID) VALUES (case_index, case_index, 0,0,'2022-06-01 12:06:54','2022-06-01 12:07:12',215,1,1,1,0,0);
		INSERT INTO sqlite_metadata.casemember (CaseID, DepartmentID, UserID, CreatedOn, CreatedBy, LastUpdatedOn, LastUpdatedBy, ProfileID) VALUES (case_index, 0, 215, '2022-06-01 12:06:54', 215, '2022-06-01 12:07:12', 215, 1);
        SET i = i + 1;
		SET case_index = case_index + 1;
    END WHILE;
END //
delimiter ;
```
cases_amount: Number of cases you want to create
case_index: The last case ID in the Sql table- `sqlite_metadata.investigationheader`

**For Tasks:**

```
delimiter //
CREATE PROCEDURE myprocTask()
BEGIN
DECLARE i int DEFAULT 0;
DECLARE Tasks_amount int DEFAULT XXX;
DECLARE Tasks_index int DEFAULT XXXX;
    WHILE (i <= Tasks_amount) DO
         INSERT INTO sqlite_metadata.ta9task (id, title, department, assignee, status, priority, type, 
         related_case, due_date, created_by, create_date, private) VALUES (task_index, task_index, '0', '263', '1', '1', '8','0', '2000-04-01 00:00:00', '263', '2020-03-01 15:39:38', '0')
         SET Tasks_index = Tasks_index + 1;
    END WHILE;
END //
delimiter ;
```
Tasks_amount: Number of tasks you want to create
Tasks_index: The last task ID in the Sql table- `sqlite_metadata.ta9task`


1.Run the script to create this procedure
2.After you created the procedure Run this to call and run the procedure :

**For cases:** `call myproccase()`
**For tasks:** `call myprocTask()`

**Note!** After running the script , procedure will created and saved in the mysql . so you can create it just one time in this name , if you want to change the script and create it again you should first delete it .

**To delete the procedure :**

1. Click on 'Stored Procedures' under 'Sqlite_metadata'

2. Find the procedure you created and right click.

3. Click on Drop Stored Procedure.

![image.png](/.attachments/image-4dfe1cc6-1a1e-4400-b561-24a67008592a.png)