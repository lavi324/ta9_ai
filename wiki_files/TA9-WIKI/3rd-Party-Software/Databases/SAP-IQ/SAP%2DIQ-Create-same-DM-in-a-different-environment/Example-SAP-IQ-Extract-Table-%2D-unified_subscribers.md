[[_TOC_]]

## Get all tables:
```exec sp_tables '%', 'DBA', '%', "'TABLE'"```

# 1. Open InteactiveSQL on running ENV
```
select g.table_name, g.column_name, g.domain_name as type, g.width
from(
select *
from
(select a.table_id, a.table_name, b.column_name, b.domain_id, b.width
from systab a
JOIN systabcol b
on a.table_id = b.table_id
where a.table_name = 'unified_subscribers') c
JOIN
SYS.SYSDOMAIN d
on d.domain_id = c .domain_id) g;
```

# 2. Copy Rows: 

![image.png](/.attachments/image-df2891d5-32a0-40dd-b93f-21dd65bbaf21.png)


# 3. Open Excel


Paste the content of rows:
=CONCAT(A1," ",B1,"(",C1,"),")
=CONCAT(A2," ",B2,"(",C2,"),")


![image.png](/.attachments/image-51752b34-44a1-469c-ab71-59b7f3c509e1.png)

Fill all other.

# 4. fix some errors:


```
for timestamp delete (*):
delete all: '
add ( in the first line
add ); in the end of the file
for integer change to int
for all date(*) change to > DATETIME
for the last statement delete: ,
if there is double delete(*)
```


# Run on local ENV

## Should look like this

CREATE TABLE unified_subscribers(

LastUpdate DATETIME,
Row_ID int,
NUMERO_PIECE varchar(110),
FULLNAME varchar(255),
DATE_NAISSANCE DATETIME,
LIEU_NAISSANCE varchar(255),
SEXE varchar(45),
ADRESSE_GEOGRAPHIQUE varchar(255),
NUMERO_TELEPHONE varchar(25),
ADRESSE_POSTALE varchar(255),
PAYS_ORIGINE varchar(55),
EMAIL varchar(255),
PHOTO_FILENAME varchar(255),
RECTO_FILENAME varchar(255),
VERSO_FILENAME varchar(255),
DATE_IDENTIFICATION DATETIME,
CODE_TYPE_PIECE varchar(15),
PHONE_TYPE varchar(7),
WEB_SITE varchar(255),
DataSource varchar(15),
NOM varchar(255),
PRENOMS varchar(255),
IndexDate timestamp
);



 







