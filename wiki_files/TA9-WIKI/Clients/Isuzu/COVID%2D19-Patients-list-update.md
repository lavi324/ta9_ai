Once a new patient list is uploaded to the system, there's a need to update the new rows with the following Values:
1. Record ID (Where RecordID=Null)
2. IsActive=YES
3. Insert date

To do so, we can run the following script via IQ:

**update Covid_19_Patients_Quarantine
    set RecordID = number()+ (select max(RecordID) from Covid_19_Patients_Quarantine), IsActive = 1, insert_date = CURRENT DATE
    where RecordID is null;**


In case a patient found on the Covid-19 but not found on GeoFencing:
1. Validate that the CDR holds CDR's from the last 10 hours.
2. Validate the patient has "Base location" data in the Covid 19 patients list.
3. If no base location is reported run the function:
call calc_base_locations(-7)

This will recalculate the base location based on the last 7 days from CDR.


## Update script

###Login as root
```
mkdir -p /covid-19 && cd /covid-19
touch covid-19-update.sh
chmod +x covid-19-update.sh
chmod 755 covid-19-update.sql
vi covid-19-update.sh
```

### Paste this:
```
#################################################
# This Script will run covid-19 update          #
# Written By: Maor Paz                          #
# Version : 1.0.0                               #
# Date: 10/09/2020                              #
#################################################
#!/bin/bash
SYBASE=/opt/application/iq16/
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/opt/application/iq16/jre/bin:/opt/application/iq16/IQ-16_0/bin64
JAVA_HOME=/opt/application/iq16/jre

su - iq16 -c "isql -Udba -P'ivoryIQ\$#data' -S10.100.102.95:2638 -b -n -o /home/iq16/result*.log" <<- EOF >/dev/null
update covid_19_Patients_Quarantine
set RecordID = number()+ (select max(RecordID) from Covid_19_Patients_Quarantine),
IsActive = 1,
insert_date = CURRENT DATE
where RecordID is null
go
exit
EOF

mv /home/iq16/result.log /home/iq16/result$(date -d "today" +"%Y%m%d%H%M").log

```
![image.png](/.attachments/image-984e7675-b054-458c-8891-3093f12aa1d7.png)