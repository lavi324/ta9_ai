# **STEPS:**

## Get the table headers:
Right-Click on the original table you want to copy in the MySql Workbench of the original environment  - 

![image.png](/.attachments/image-216af87a-ef26-4c7d-b4cd-7374c091255f.png)

## Create table in the new ENV:
Then, paste it into the relevant environment you wish to have the table in (make sure it's in the same schema) -

![image.png](/.attachments/image-820a08d3-ed19-47b6-815d-570538b358b0.png)

For Example : 
```
CREATE TABLE `vehicules` (
  `Column1` varchar(500) DEFAULT NULL,
  `Column2` varchar(500) DEFAULT NULL,
  `DATE_MISE_CIRCULATION` datetime DEFAULT NULL,
  `DATE_EDITION` datetime DEFAULT NULL,
  `MARQUE` varchar(500) DEFAULT NULL,
  `GENRE` varchar(500) DEFAULT NULL,
  `COULEUR` varchar(500) DEFAULT NULL,
  `CARROSSERIE` varchar(500) DEFAULT NULL,
  `ENERGIE` varchar(500) DEFAULT NULL,
  `USAGE_VEHICULE` varchar(500) DEFAULT NULL,
  `NOMBRE_ESSIEUX` decimal(9,4) DEFAULT NULL,
  `PLACES_ASSISES` decimal(9,4) DEFAULT NULL,
  `PUISSANCE_FISCALE` decimal(9,4) DEFAULT NULL,
  `CYLINDREE` decimal(9,4) DEFAULT NULL,
  `PESO_BRUTO` decimal(9,4) DEFAULT NULL,
  `CODE_TYPE_PIECE` varchar(500) DEFAULT NULL,
  `NUMERO_PIECE` varchar(500) DEFAULT NULL,
  `Column3` varchar(500) DEFAULT NULL,
  `NUMERO_CHASSIS` varchar(500) DEFAULT NULL,
  `fileid` int(11) DEFAULT NULL,
  `caseid` int(11) DEFAULT NULL,
  `departmentid` int(11) DEFAULT NULL,
  `system_comment` varchar(1024) DEFAULT NULL,
  KEY `Index_VEHICULES_NUMERO_CHASSIS` (`NUMERO_CHASSIS`(50)),
  KEY `Index_VEHICULES_TYPE_TECHNIQUE` (`TYPE_TECHNIQUE`(50)),
  KEY `Index_VEHICULES_CHARGE_UTILE` (`CHARGE_UTILE`),
  KEY `Index_VEHICULES_PTAC` (`PTAC`),
  KEY `Index_VEHICULES_IMMATRICULATION_PRECEDENTE` (`IMMATRICULATION_PRECEDENTE`(50)),
  KEY `Index_VEHICULES_fileid` (`fileid`),
  KEY `Index_VEHICULES_caseid` (`caseid`),
  KEY `Index_VEHICULES_departmentid` (`departmentid`),
  KEY `Index_VEHICULES_system_comment` (`system_comment`(50))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
```
Make sure there are 4 mandatory system fields (case-sensitive):
- fileid
- caseid
- departmentid
- system_comment

## Create DM in the _Admin Studio_ based on this table:

1. Click on the Data models tile
2. Click on 'Add Data Connection'
3. Click on 'MySql'
4. Enter Credentials to connect
5. choose the relevant Schema and Table
6. Save

