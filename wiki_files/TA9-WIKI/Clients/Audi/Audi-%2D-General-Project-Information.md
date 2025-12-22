[[_TOC_]]

#Site Book

Link to SiteBook (created by rayzone):
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/Shared%20Documents/Projects/Audi/Site%20Book/AZR%20Taxes%20-%20Site%20Book%20Draft%20v0.2.docx?d=wd184917b0a1d4ef7ba3c66d206d1cf56&csf=1&web=1&e=7XiUqI


#Installation

##Installation SOW (created by TA9):
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B82B7EE03-7489-4BD3-B112-09917D0AECCC%7D&file=Audi%20installation.docx&action=default&mobileredirect=true

#46140
#46194

##The stages

1. Local home preparation and validation of the SW.
2. Services Installation.
3. File server installation.
4. Wildfly installation.
5. Mysql DB installation.
6. Orient DB Installation.
7. Solr installation.
8. TA9 Run time installation.
9. Environment basic testing.

##The tests

The environment basic testing:
1. Login with the Admin user
1. Querying DM 
1. Load Data to DM – A simple DM that consists of 2 columns (Name, ID)
1. Create entities
1. Create relations – A two-way ‘Relationship’ between 2 persons

#DB connection to STG
#46401
1. connect to VPN
2. go to remote desktop - IP 10.122.75.1
- connect with your username and password (same as login to the VPN)
3. while in 10.122.75.1 - go to remote desktop 10.122.75.9
4. connect -
- User name: .\administrator
- password is T22vm9#$
5. go to chrome 
6. log in to portal-test.ta9.taxes.gov.az

#Connect to production Data Base
#46238

following are the instructions on how to connect to replica of production report DB:

1. Connect to VPN with your user
2. Connect via RDP to dedicated windows machine that has TOAD tool installed
- Ip - 10.122.75.1
- Username – same as vpn username + "@system.local"
- Password – same as vpn password
3. Launch TOAD application
- If the application asks to re enter license key, license key data is located on the same server in the C:\Toad\Toad_license_key.txt.TXT file
4. Connect to the database
use the following credentials
- IP: 10.22.12.213
- port: 1521
- user: ta9
- pass: 04l2rsmj621vs8
- SID: repalfa
5. to insert the MV Scripts:
- schema browser (second icon from the left)
- Firs row: to select the name of the wanted MV (for example - "AIST_REP_DATA")
- Second row: to select "Materialized views"
- third row: the name of the wanted MV )for example - "mv_taxpayer")
- on the right window - select the tab "Script".
- Query relevant tables from attached Shamsudin email
- For example select count(*) from AVIS_DATA.MV_UTL_PERSON
- To browse schema, and check columns and statistics as well as sample data go to schema explorer and look under AVIS_DATA schema (in top menu under Database -> Schema Browser select AVIS_DATA, Tables and * to see all tables)

#Oracle DB Admin Studio Connection Configuration
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/722/Oracle-DB-Admin-Studio-Connection-Configuration


#VPN
##Users
Oren Lugashi Oren@t-a9.com
Noga Segev noga.segev@t-a9.com
Liza Tsenin liza.tsenin@t-a9.com
Dekel Mottin dekel.mottin@t-a9.com
Almog Hillel almog.hillel@t-a9.com
Natalia Kostenkov natalia.kostenkov@t-a9.com
Bar Kadosh Bar.Kadosh@t-a9.com
Ronielle Kabakov Ronielle@t-a9.com
Hai Gatenyo Hai@t-a9.com
Bar Hickri bar.hickri@t-a9.com
Alex Kovalyov alex.kovalyov@t-a9.com
Orel Bezalel orel.bezalel@t-a9.com

Credentials can be found on Passbolt account.

##Install Guide

Connect using Cisco AnyConnect Secure mobility client – you can download it from the official Cisco site.
Client download link: https://mega.nz/folder/E1JTQSKA#nBTStWQzgyfTVtUQBPAvlw


VPN connection:
![vpn.png](/.attachments/vpn-e012b605-d036-4b7d-8cf8-cd6304260771.png)


| Cisco AnyConnect: | cvpn.e-taxes.gov.az |
|--|--|
| Group: | External_Users |

For Password Reset:
 
http://10.130.111.1/iisadmpwd/changepasswordnow.asp
 
http://10.122.111.1/iisadmpwd/changepasswordnow.asp


